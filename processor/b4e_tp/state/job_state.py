import logging

from addressing.b4e_addressing import addresser

from protobuf.b4e_protobuf import job_pb2

LOGGER = logging.getLogger(__name__)


def get_job(self, job_id, company_public_key, candidate_public_key):
    try:
        address = addresser.get_job_address(job_id, company_public_key, candidate_public_key)
        state_entries = self._context.get_state(
            addresses=[address], timeout=self._timeout)
        if state_entries:
            container = job_pb2.JobContainer()
            container.ParseFromString(state_entries[0].data)
            for job in container.entries:
                if job.job_id == job_id and job.company_public_key == company_public_key and job.candidate_public_key == candidate_public_key:
                    return job

        return None
    except Exception as e:
        print("Err :", e)
        return None


def set_job(self, job):
    address = addresser.get_job_address(job.job_id, job.company_public_key, job.candidate_public_key)

    container = job_pb2.JobContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)

    container.entries.extend([job])
    data = container.SerializeToString()

    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)


def set_job_end(self, job_id, company_public_key, candidate_public_key, end):
    address = addresser.get_job_address(job_id, company_public_key, candidate_public_key)

    container = job_pb2.JobContainer()
    state_entries = self._context.get_state(
        addresses=[address], timeout=self._timeout)
    if state_entries:
        container.ParseFromString(state_entries[0].data)
        for job in container.entries:
            if job.job_id == job_id and job.candidate_public_key == candidate_public_key and job.company_public_key == company_public_key:
                # LOGGER.info("update end job")
                job.end.CopyFrom(end)

    data = container.SerializeToString()
    updated_state = {}
    updated_state[address] = data
    self._context.set_state(updated_state, timeout=self._timeout)
    pass
