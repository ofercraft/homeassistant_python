import time
from requests import post

default_url = ("<YOUR_HOME_ASSISTANT_URL>")
default_token = "<YOUR_HOMEASSISTANT_LONG_LIVED_ACCESS_TOKEN>"


def service_call(service, data, url=default_url, token=default_token):
    headers = {
        "Authorization": f"Bearer {token}"}

    request_service = str(service).replace('.', '/')
    request_url = (f"{url}/api/services/{request_service}")
    response = post(request_url, headers=headers, json=data)
    return response


def control_switch(state, switch, url=default_url, token=default_token):
    if state == "on" or state == "toggle" or state == "off":
        if not switch.startswith("switch."): switch = f"switch.{switch}"
        if state == "on" or state == "off": state = f"turn_{state}"
        response = service_call(f"switch.{state}", {"entity_id": switch}, url=url, token=token).text
    else:
        response = False
    return response


def control_light(state, light, url=default_url, token=default_token):
    if state == "on" or state == "toggle" or state == "off":  # check if state is valid (on / toggle / off).
        if not light.startswith(
                "light."): light = f"light.{light}"  # check if light comes full, if not add the start (light.)
        if state == "on" or state == "off": state = f"turn_{state}"  # turn state (on / off) to valid states.
        response = service_call(f"light.{state}", {"entity_id": light}, url=url,
                                token=token).text  # call the homeassistant api
    else:
        response = False
    return response  # return the response


def control_climate(state, climate, temp=False, mode=False, url=default_url,
                    token=default_token):  # control a climate device
    response = False
    if state == "on" or state == "toggle" or state == "off":  # check if state is valid (on / toggle / off).
        if not climate.startswith(
                "climate."): climate = f"climate.{climate}"  # check if target comes with full full, if not add the start (climate.)
        if state == "on" or state == "off": state = f"turn_{state}"  # turn state (on / off) to valid states.
        if not temp and not mode:
            response = service_call(f"climate.{state}", {"entity_id": climate}, url=url,
                                    token=token).text  # call the homeassistant api


    else:
        response = False
    return response  # return the response
