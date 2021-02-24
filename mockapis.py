## Mocking FastAPI APIs so we can continue to develop
## These API's have to be implemented in FastAPI before deploy

sidebar_items = [
    {
        "text": "Inventory",
        "href": "#",
        "subheaders": [
            {"text": "Excess Manager", "href": "#"},
            {"text": "Excess Dashboards", "href": "#"},
            {"text": "Documentation", "href": "#"},
        ],
    },
    {
        "text": "ACOE",
        "href": "#",
        "subheaders": [
            {"text": "About", "href": "#"},
            {"text": "SchedulerUI", "href": "#"},
        ],
    },
]

job_1 = {
    "name": "print_hello",
    "func_args": [],
    "created_at": "2021-02-15T09:42:47.285258+00:00",
    "owner": "jon.snow@example.com",
    "timeout": 3600,
    "crons": [],
    "func_kwargs": {},
    "function": "891970d0-9457-4db3-8351-36e224f90f35",
    "upstream": {},
    "description": None,
    "downstream": {"print_hello": "success"},
}

job_2 = {
    "name": "salary_data_validation",
    "func_args": [],
    "created_at": "2021-02-09T12:54:52.156548+00:00",
    "owner": "arya.stark@example.com",
    "timeout": 3600,
    "crons": [],
    "func_kwargs": {},
    "function": "04fe47a4-15ea-42ed-884c-c59c8aace7f4",
    "upstream": {"print_hello": "success"},
    "description": "Data validation",
    "downstream": {},
}

job_3 = {
    "name": "test_job",
    "func_args": [],
    "created_at": "2021-02-22T09:42:47.285258+00:00",
    "owner": "daenerys.targaryen@example.com",
    "timeout": 3600,
    "crons": [],
    "func_kwargs": {},
    "function": "891970d0-9457-4db3-8351-36e224f90f35",
    "upstream": {},
    "description": None,
    "downstream": {},
}

job_4 = {
    "name": "test_job_2",
    "func_args": [],
    "created_at": "2021-02-15T12:54:52.156548+00:00",
    "owner": "daenerys.targaryen@example.com",
    "timeout": 3600,
    "crons": [],
    "func_kwargs": {},
    "function": "04fe47a4-15ea-42ed-884c-c59c8aace7f4",
    "upstream": {},
    "description": None,
    "downstream": {},
}


jobs = {"data": [job_1, job_2, job_3, job_4]}
