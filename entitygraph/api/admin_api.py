import io
from pathlib import Path

from entitygraph.base_client import BaseApiClient


class AdminAPI(BaseApiClient):
    # jobs-ctrl
    def exec_replace_subject_identifiers_job(self, application_label='default'):
        endpoint = "/api/admin/jobs/execute/normalize/subjectIdentifiers"
        headers = {'X-Application': application_label}
        return self.make_request('POST', endpoint, headers=headers)

    def exec_replace_object_identifiers_job(self, application_label='default'):
        endpoint = "/api/admin/jobs/execute/normalize/objectIdentifiers"
        headers = {'X-Application': application_label}
        return self.make_request('POST', endpoint, headers=headers)

    def exec_export_job(self, application_label='default'):
        endpoint = "/api/admin/jobs/execute/export"
        headers = {'X-Application': application_label}
        return self.make_request('POST', endpoint, headers=headers)

    def exec_deduplication_job(self, application_label='default'):
        endpoint = "/api/admin/jobs/execute/deduplication"
        headers = {'X-Application': application_label}
        return self.make_request('POST', endpoint, headers=headers)

    def exec_coercion_job(self, application_label='default'):
        endpoint = "/api/admin/jobs/execute/coercion"
        headers = {'X-Application': application_label}
        return self.make_request('POST', endpoint, headers=headers)

    # admin

    def import_file(self, mimetype, file_path: Path, application_label='default'):
        endpoint = "/api/admin/bulk/import/file"
        headers = {'X-Application': application_label}
        params = {'mimetype': mimetype}
        with open(file_path, 'rb') as file_mono:
            files = {'fileMono': (file_path.name, file_mono)}
            return self.make_request('POST', endpoint, params=params, headers=headers, files=files)

    def import_entities(self, mimetype, rdf_data: str, application_label='default'):
        endpoint = "/api/admin/bulk/import/entities"
        headers = {'X-Application': application_label, 'Content-Type': 'application/octet-stream'}
        params = {'mimetype': mimetype}
        data = io.BytesIO(rdf_data.encode())
        return self.make_request('POST', endpoint, params=params, headers=headers, data=data)

    def reset_repository(self, name, application_label='default'):
        endpoint = "/api/admin/bulk/reset"
        headers = {'X-Application': application_label}
        params = {'name': name}
        return self.make_request('GET', endpoint, params=params, headers=headers)