
import time

from requests import Session
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

disable_warnings(InsecureRequestWarning)


URL = 'https://rebrickable.com/api/v3/'


def _get_api(url, endpoint, params='', headers=None, token=''):
    if not headers:
        headers = {
            'Authorization': token,
            # "Content-Type": "application/json"
        }

    uri = url + endpoint + params

    with Session() as session:
        try:
            response = session.get(
                uri,
                headers=headers,
                verify=False
            )
            if response.status_code == 200:
                res = response.json()
            else:
                res = response.text

            if response.status_code != 200:
                print(f'Status: {response.status_code}')
                print(res)

            time.sleep(1)
            return response.status_code, res

        except Exception as e:
            print("API GET / Parse Error:  {}".format(e))
            return None


def get_element(token, element_id):
    """
    Get element info

    :param token: token for Rebrickable API
    :param element_id: number of the part (as in the parts-list
    :return: API result
    """

    res_stat, res = _get_api(
        token='key ' + token,
        url=URL,
        endpoint=f'lego/elements/{str(element_id)}'
    )
    return res


def get_set(token, set_num):
    """
    Get Lego-set info

    :param token: token for Rebrickable API
    :param set_num: number of the set
    :return: API result
    """

    if '-' not in set_num:
        set_num += '-1'

    res_stat, res = _get_api(
        token='key ' + token,
        url=URL,
        endpoint=f'lego/sets/{str(set_num)}'
    )
    return res, res_stat


def get_theme(token, theme_id):
    """
    Get Lego-theme

    :param token: token for Rebrickable API
    :param theme_id: id of the theme
    :return: Name of the theme
    """

    res_stat, res = _get_api(
        token='key ' + token,
        url=URL,
        endpoint=f'lego/themes/{str(theme_id)}'
    )
    return res['name']
