# API Documentation

## Base URL

```
http://localhost:5000/api
```

## Endpoints

### Health Check

**GET** `/health`

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "ngrok-api"
}
```

### List Tunnels

**GET** `/tunnels`

Get all active tunnels.

**Response:**
```json
{
  "tunnels": [
    {
      "name": "http_8000",
      "public_url": "https://abc123.ngrok.io",
      "status": "active"
    }
  ],
  "count": 1
}
```

### Create Tunnel

**POST** `/tunnels`

Create a new tunnel.

**Request Body:**
```json
{
  "protocol": "http",
  "local_addr": "localhost",
  "local_port": 8000,
  "name": "my_tunnel"
}
```

**Response (201):**
```json
{
  "name": "my_tunnel",
  "public_url": "https://abc123.ngrok.io",
  "protocol": "http",
  "local_addr": "localhost",
  "local_port": 8000,
  "status": "active"
}
```

### Get Tunnel

**GET** `/tunnels/{name}`

Get information about a specific tunnel.

**Response:**
```json
{
  "name": "my_tunnel",
  "public_url": "https://abc123.ngrok.io",
  "status": "active"
}
```

### Delete Tunnel

**DELETE** `/tunnels/{name}`

Close a tunnel.

**Response (200):**
```json
{
  "message": "Tunnel my_tunnel closed"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required fields"
}
```

### 404 Not Found
```json
{
  "error": "Not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```