# Giotto

<p>
<a href="https://github.com/acivitillo/giotto/actions?query=workflow%3ABuild" target="_blank">
    <img src="https://github.com/acivitillo/giotto/workflows/Build/badge.svg" alt="Build">
</a>

<a href="https://github.com/psf/black" target="_blank">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Build">
</a>
</p>

![alt-text](https://github.com/acivitillo/giotto/blob/main/docs/giotto.gif)

## Running the examples

Please make sure that you have `HTTP_PROXY` in your environment variables if needed.

To run the Server:

```bash
uvicorn main:webapp.app --reload
```

Examples are running on these urls:

* http://127.0.0.1:8000/scheduler
* http://127.0.0.1:8000/ghpage
* http://127.0.0.1:8000/frames


## How to contribute?

Please follow the instructions in [contributing guidelines](https://github.com/acivitillo/giotto/blob/main/CONTRIBUTING.md).