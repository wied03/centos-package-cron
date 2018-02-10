1. Unit tests are important!
2. Ensure changelog is updated
3. Bump the version in `setup.py`
4. Create a GitHub tag

```shell
rake build push
```

Then upload the RPMS from the `built_rpms` directory to the Github release.
