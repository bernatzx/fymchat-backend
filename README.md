Development vs Production running

| Environment | API URL                   | Cara menjalankan                           |
| ----------- | ------------------------- | ------------------------------------------ |
| Local PC    | `http://127.0.0.1:8000`   | `uvicorn main:app --reload`                |
| Expo + HP   | `http://IP-PC:8000`       | `uvicorn main:app --reload --host 0.0.0.0` |
| Production  | `https://api.example.com` | Uvicorn + Nginx + systemd                  |