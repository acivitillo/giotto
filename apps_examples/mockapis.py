## Mocking FastAPI APIs so we can continue to develop
## These API's have to be implemented in FastAPI before deploy

sidebar_items = [
    {
        "text": "Documentation",
        "href": "#",
        "subheaders": [
            {"text": "Giotto Readme", "href": "/ghpage/"},
            {"text": "Example link", "href": "#"},
        ],
    },
    {
        "text": "ACOE",
        "href": "#",
        "subheaders": [
            {"text": "Scheduler", "href": "/scheduler/"},
            {"text": "Connected Frames", "href": "/frames/"},
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
    "downstream": {"salary_data_validation": "success"},
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


jobs = {"data": 500 * [job_1, job_2, job_3, job_4]}


jobruns_raw = {
    "print_hello": {
        "data": [
            {
                "id": "1",
                "name": None,
                "created_at": "2021-02-16T11:08:27.605965+00:00",
                "dask_scheduler_address": None,
                "finished_at": "2021-02-16T11:08:30.943572+00:00",
                "duration": 3,
                "status": "killed",
                "logs": None,
                "error": None,
                "traceback": None,
                "result": None,
            },
            {
                "id": "2",
                "name": None,
                "created_at": "2021-02-16T11:16:12.840809+00:00",
                "dask_scheduler_address": None,
                "finished_at": "2021-02-16T11:16:17.572336+00:00",
                "duration": 4,
                "status": "killed",
                "logs": None,
                "error": None,
                "traceback": None,
                "result": None,
            },
            {
                "id": "3",
                "name": None,
                "created_at": "2021-02-16T14:12:40.387612+00:00",
                "dask_scheduler_address": None,
                "finished_at": "2021-02-16T14:13:10.625563+00:00",
                "duration": 30,
                "status": "success",
                "logs": "",
                "error": None,
                "traceback": None,
                "result": 1,
            },
        ]
    },
    "salary_data_validation": {"data": []},
    "test_job": {"data": []},
    "test_job_2": {
        "data": [
            {
                "id": "1",
                "name": None,
                "created_at": "2021-02-16T11:01:59.930253+00:00",
                "dask_scheduler_address": None,
                "finished_at": "2021-02-16T11:02:06.559968+00:00",
                "duration": 7,
                "status": "success",
                "logs": "",
                "error": None,
                "traceback": None,
                "result": None,
            },
            {
                "id": "2",
                "name": None,
                "created_at": "2021-02-16T11:07:55.353094+00:00",
                "dask_scheduler_address": None,
                "finished_at": "2021-02-16T11:08:01.762987+00:00",
                "duration": 5,
                "status": "success",
                "logs": "",
                "error": None,
                "traceback": None,
                "result": None,
            },
        ]
    },
}


jobruns = {"data": []}

for job_name, data in jobruns_raw.items():
    jobruns["data"].extend(data["data"])


sources = {
    "redshift": {
        "music": {"track": [], "artist": []},
        "mathematics": {"squares": [], "integrals": []},
        "cities": {"london": ["street", "building", "price"]},
    },
    "aurora": {
        "music": {"track": [], "artist": []},
        "dance": {"rumba": ["move", "time"], "tango": ["move", "time"], "salsa": ["move", "time"]},
    },
}


records = [
    ["redshift", "music", "track", "id"],
    ["redshift", "mathematics", "squares", "area"],
    ["redshift", "mathematics", "integrals", "formula"],
    ["redshift", "cities", "london", "street"],
    ["redshift", "cities", "london", "building"],
    ["redshift", "cities", "london", "price"],
    ["aurora", "music", "track", "id"],
    ["aurora", "music", "artist", "name"],
    ["aurora", "dance", "rumba", "move"],
    ["aurora", "dance", "rumba", "time"],
    ["aurora", "dance", "tango", "move"],
    ["aurora", "dance", "tango", "time"],
    ["aurora", "dance", "salsa", "move"],
    ["aurora", "dance", "salsa", "time"],
]

sources = {"source": [], "schema": [], "table": [], "column": []}
for record in records:
    for index, value in enumerate(sources.values()):
        value.append(record[index])