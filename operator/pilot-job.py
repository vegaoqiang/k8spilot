import sys
import time
import kubernetes

TAINT_KEY = "node.k8spilot.io/network-not-ready"
TAINT_VALUE = "true"
TAINT_EFFECT = "NoSchedule"


def get_calico_pod_status_by_node(corev1, node_name) -> bool:
	try:
		pods = corev1.list_pod_for_all_namespaces(
			field_selector=f"spec.nodeName={node_name}",
			label_selector="k8s-app=calico-node"
		)
	except kubernetes.client.ApiException as e:
		print(e)
		return False
	
	if not pods.items:
		return False
    
	pod = pods.items[0]
	if pod.status.phase != "Running":
		return False
	
	for cond in pod.status.conditions or []:
		if cond.type == "Ready":
			return True if cond.status == "True" else False
	
	return False


def ensure_taint(corev1, node) -> None:
	taints = node.spec.taints or []
	if any(t.key == TAINT_KEY for t in taints):
		return
	taints.append(kubernetes.client.V1Taint(
		key=TAINT_KEY,
		value=TAINT_VALUE,
		effect=TAINT_EFFECT
	))
	body = {"spec": {"taints": [t.to_dict() for t in taints]}}
	corev1.patch_node(node.metadata.name, body)
	print(f"Make taint {TAINT_KEY} on node {node.metadata.name}")


def remove_taint(corev1, node) -> None:
	taints = node.spec.taints or []
	new_taints = [t for t in taints if t.key != TAINT_KEY]
	if len(new_taints) != len(taints):
		body = {"spec": {"taints": [t.to_dict() for t in new_taints]}}
		corev1.patch_node(node.metadata.name, body)
		print(f"Remove taint {TAINT_KEY} on node {node.metadata.name}")

def main():
	kubernetes.config.load_incluster_config()
	corev1 = kubernetes.client.CoreV1Api()

	nodes = corev1.list_node().items
	for node in nodes:
		if not get_calico_pod_status_by_node(corev1, node.metadata.name):
			print(f"Calico NotReady on {node.metadata.name}")
			ensure_taint(corev1, node)

	while True:
		all_ready = True
		for node in corev1.list_node().items:
			if not get_calico_pod_status_by_node(corev1, node.metadata.name):
				print(f"Calico NotReady on {node.metadata.name}")
				all_ready = False
			else:
				print(f"Calico Ready on {node.metadata.name}")
				remove_taint(corev1, node)
		if all_ready:
			break
		time.sleep(10)

	sys.exit(0)

if __name__ == '__main__':
	main()