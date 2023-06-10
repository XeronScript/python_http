from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import List, Dict


class WarehouseHTTPServer(BaseHTTPRequestHandler):
    def _set_response(self, status_code=200, headers=None) -> None:
        self.send_response(status_code)
        if headers:
            for key, value in headers.items():
                self.send_header(key, value)
        self.end_headers()

    def do_GET(self) -> None:
        if self.path == '/':
            self._set_response()
            self.wfile.write(b'Welcome to the warehouse HTTP Server!')
        else:
            warehouse_ids = self.path.strip('/').split(',')
            try:
                products = self.get_product_from_warehouse(warehouse_ids)
                if products:
                    response_body = self.generate_html_table(products)
                    self._set_response()
                    self.wfile.write(response_body.encode('utf-8'))
                else:
                    self._set_response(status_code=404)
                    self.wfile.write(b'No product found for the specified warehouses.')
            except ValueError:
                self._set_response(status_code=400)
                self.wfile.write(b'Invalid warehouse ID format. Please provide comma-separated numbers.')

    def get_product_from_warehouse(self, warehouse_ids: List[str]) -> List[Dict[str, str]]:
        database = self.read_database()
        products = []
        for line in database:
            line = line.strip().split(',')
            warehouse_id = line[0]
            if warehouse_id[-1] in warehouse_ids:
                product = line[1]
                quantity = line[2]
                products.append({'product': product, 'quantity': quantity})
        return products

    def generate_html_table(self, products: List[Dict[str, str]]) -> str:
        table_rows = []
        total_quantity = 0

        for product in products:
            table_row = f"<tr><td>{product['product']}</td><td>{product['quantity']}</td></tr>"
            table_rows.append(table_row)
            total_quantity += int(product['quantity'])

        return f"""
            <html>
            <head>
                <style>
                    table {{ border-collapse: collapse; }}
                    th, td {{ border: 1px solid black; padding: 5px; }}
                </style>
            </head>
            <body>
                <table>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                    </tr>
                    {''.join(table_rows)}
                </table>
                <strong><p>Summary quantity: {total_quantity}</p></strong>
            </body>
            </html>
        """

    def read_database(self) -> List[str]:
        try:
            with open('database.txt', 'r') as file:
                return file.readlines()
        except FileNotFoundError:
            raise ValueError("Database file not found.")


def run(server=HTTPServer, handler=WarehouseHTTPServer, port=8000) -> None:
    server_address = ('', port)
    httpd = server(server_address, handler)
    print(f'Server is listening on {server_address}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
