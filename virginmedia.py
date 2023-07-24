from requests import Session
from json import dumps
import logging


class VirginMediaException(Exception):
    pass


class VirginMedia:

    _auth: str
    _base: str
    _token: str
    _session: Session

    def __init__(self, base: str = 'http://192.168.0.1'):
        self._session = Session()
        self._base = base

    def auth(self, password):
        self._auth = password

        resp = self._post('/rest/v1/user/login', {
            'password': self._auth
        })
        print(resp)

        if 'created' in resp:
            self.set_token(resp['created']['token'])

    def set_token(self, token):
        self._token = token
        self._session.headers.update({
            'Authorization': f'Bearer {self._token}'
        })

    def _post(self, endpoint: str, data: dict) -> dict:
        r = self._session.post(
            f'{self._base}{endpoint}',
            headers={
                'Content-Type': 'application/json'
            },
            data=dumps(data)
        )

        if r.status_code == 400:
            raise VirginMediaException(f'Bad request. {r.text}')

        return r.json()

    def _request(self, endpoint: str) -> dict:
        r = self._session.get(f'{self._base}{endpoint}')

        if r.status_code == 401:
            raise VirginMediaException('Authorisation error')

        print(r.text)

        return r.json()

    def get_connected_devices(self):
        logging.info('Getting connected devices')
        return self._request('/rest/v1/network/hosts?connectedOnly=true')

    def get_dhcp_settings(self):
        return self._request('/rest/v1/network/ipv4/dhcp')

    def get_state(self):
        return self._request('/rest/v1/cablemodem/state_')

    def get_system_info(self):
        return self._request('/rest/v1/system/info')

    def get_gateway_provisioning(self):
        return self._request('/rest/v1/system/gateway/provisioning')


if __name__ == '__main__':
    vm = VirginMedia()
    # vm.auth('')
    vm.set_token('')
    print(dumps(vm.get_connected_devices(), indent=4))
    print(dumps(vm.get_state(), indent=4))
