# fmc_backend

Find My Coach Server

# Database

## Migrations

### Create new migration revision

```bash
alembic revision -m '<message>' --autogenerate
```

### DB migrate

```bash
alembic upgrade head
```

# How to generate messages

See list of coaches emails:

```bash
invoke get-coaches
```

See list of students emails:

```bash
invoke get-students
```

Now we have 2 options:

- if we want to send message to coach use next:

```bash
invoke message-to-coach --author=*student email* --receiver=*coach email* -- text=some random text
```

- ```bash
  invoke message-to-student --author=*coach email* --receiver=*student email* -- text=some random text
  ```

```

! --text argument is optional !
```
