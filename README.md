# django-authenticate
## deafult user model
```
| Field        | Type          | Description           |
| ------------ | ------------- | --------------------- |
| username     | CharField     | Required, unique      |
| first_name   | CharField     | Optional              |
| last_name    | CharField     | Optional              |
| email        | EmailField    | Optional              |
| password     | CharField     | Hashed password       |
| is_staff     | BooleanField  | Admin site access     |
| is_active    | BooleanField  | Active user or not    |
| is_superuser | BooleanField  | Full permissions      |
| last_login   | DateTimeField | Last login time       |
| date_joined  | DateTimeField | Account creation time |

```