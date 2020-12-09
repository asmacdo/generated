
import os
import kopf
import kubernetes
from jinja2 import Template
import pykube
import yaml
import sys
from pprint import pprint
from kubernetes.client.rest import ApiException

# kopf.config.load_kube_config()

@kopf.on.create('cache.example.com', 'v1alpha1', 'memcacheds')
# TODO delete, update
# @kopf.on.update('cache.example.com', 'v1alpha1', 'memcacheds')
def reconcile(spec, name, namespace, logger, **kwargs):
    # Render the pod yaml with some spec fields used in the template.
    # TODO(asmacdo) read this from the CR
    size = 1
    # size = spec.get('size')
    # if not size:
    #     raise kopf.PermanentError(f"Size must be set on the Memcached resource.")

    name = "huzzah"
    # TODO(asmacdo) relative path isnt working? Should not need to hardcode this path
    # with open("memcached-deployment.yaml.j2", 'r') as template_file:
    with open("/src/memcached-deployment.yaml.j2", 'r') as template_file:
        template = Template(template_file.read())
        try:
            manifest_str = template.render(name=name, size=size)
            manifest = yaml.safe_load(manifest_str)
            # TODO(asmacdo) remove this
            print(manifest)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # Make it our child: assign the namespace, name, labels, owner references, etc.
    # TODO(asmacdo) research this
    kopf.adopt(manifest)
    deployment = create_or_update_deployment(manifest)

    # Update the parent's status.
    return {'children': [deployment.metadata['uid']]}

# TODO(asmacdo) this doesnt actually do what its supposed to yet.... just creates.
def create_or_update_deployment(manifest):
    # Actually create an object by requesting the Kubernetes API.
    api = pykube.HTTPClient(pykube.KubeConfig.from_env())
    deployment = pykube.Deployment(api, manifest)
    deployment.create()
    api.session.close()
    return deployment
