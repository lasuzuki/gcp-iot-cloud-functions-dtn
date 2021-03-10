from google.cloud import iot_v1

def sense_hat(request):
    project_id = 'your_project_id'
    cloud_region = 'the_region_of_your_project'
    registry_id = 'your_registry_id'
    device_id = 'your_device_id'
    version = 0

    request_json = request.get_json()
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(project_id, cloud_region, registry_id, device_id)
    if request.args and 'message' in request.args:
        config = request.args.get('message')
        data = config.encode("utf-8")
        client.modify_cloud_to_device_config(request={"name": device_path, "binary_data": data, "version_to_update": version})
    elif request_json and 'message' in request_json:
        config = request_json['message']
        data = config.encode("utf-8")
        client.modify_cloud_to_device_config(request={"name": device_path, "binary_data": data, "version_to_update": version})
    else:
        return f'No data received!'