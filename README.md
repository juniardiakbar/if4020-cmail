# cmail (Cryptography Mail)

Penerapan Elliptic Curve Cryptography dan SHA-3 untuk Menandatangani Surel

## Request

Request pake json body ya

### 1. POST `/send`

Contoh request body

```
{
	"to": "juniardiakbar@gmail.com",
	"subject": "subject",
	"message": "ini message"
}
```

### 2. GET `/inbox`

Pake params route untuk page yang optional. Limit diset defaultnya 10
Contoh respond

```
{
  "data": [
    {
      "body": "Ini reply\r\n",
      "from": "Juniardi Akbar <juniardiakbar@gmail.com>",
      "id": "1",
      "subject": "Reply"
    },
    {
      "body": "Tes lagi\r\n",
      "from": "Juniardi Akbar <juniardiakbar@gmail.com>",
      "id": "2",
      "subject": "Ke 2"
    }
  ],
  "message": "Success get inbox",
  "status": "200"
}
```

### 3. GET `/sent`

Sama kaya inbox. Pake params route untuk page yang optional. Limit diset defaultnya 10
Contoh respond

```
{
  "data": [
    {
      "body": "ini message tes db",
      "id": "5fc52497b58b62fce5010f2e",
      "subject": "subject",
      "to": "juniardiakbar@gmail.com"
    }
  ],
  "message": "Success get sent message",
  "status": "200"
}
```

## Env

Bikin `.env` ya pake contoh yang di `.env.example`. Jangan lupa setting akun gmail biar [<i>less secure</i>](https://support.google.com/a/answer/6260879?hl=en)
