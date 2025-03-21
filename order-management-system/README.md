# Order Management System

This project is an Order Management System designed to handle the order flow in businesses such as restaurants. It allows users to place and manage orders efficiently.

## Features

- Place new orders
- Retrieve existing orders
- Update order status
- Middleware for authentication

## Project Structure

```
order-management-system
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── __init__.py
│   │   └── order.py
│   ├── schemas
│   │   ├── __init__.py
│   │   └── order.py
│   ├── controllers
│   │   ├── __init__.py
│   │   └── order_controller.py
│   ├── routes
│   │   ├── __init__.py
│   │   └── order_routes.py
│   ├── middlewares
│   │   ├── __init__.py
│   │   └── auth_middleware.py
│   └── tests
│       ├── __init__.py
│       ├── test_main.py
│       └── test_order.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd order-management-system
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
uvicorn app.main:app --reload
```

You can access the API at `http://127.0.0.1:8000`.

## API Endpoints

- `POST /orders`: Create a new order
- `GET /orders/{order_id}`: Retrieve an order by ID
- `PUT /orders/{order_id}`: Update an existing order

## Testing

To run the tests, use the following command:
```
pytest app/tests
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License.