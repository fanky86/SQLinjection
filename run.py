import requests

# Input URL yang akan diuji
url = input("Masukkan URL yang akan diuji (contoh: http://testphp.vulnweb.com/listproducts.php?cat=): ")

# Baca payload SQL dari file
sql_payloads = []
with open('sqlattack.txt', 'r') as filehandle:
    for line in filehandle:
        sql_payload = line.strip()
        sql_payloads.append(sql_payload)

# Fungsi untuk mencetak hasil dengan tampilan kotak dan berwarna
def print_result(status, payload, message, color_code):
    print("\033[{}m".format(color_code) + f"\n{'='*40}")
    print(f"  {status} : {payload}")
    print(f"  Pesan : {message}")
    print(f"{'='*40}\033[0m")

# Cek setiap payload
for payload in sql_payloads:
    full_url = url + payload
    print("\033[1;34mTesting: {}\033[0m".format(full_url))
    
    try:
        response = requests.post(full_url)
        
        if "mysql" in response.text.lower():
            print_result("Injectable MySQL detected", payload, "Possible SQL Injection", "1;32")
        elif "native client" in response.text.lower():
            print_result("Injectable MSSQL detected", payload, "Possible SQL Injection", "1;33")
        elif "syntax error" in response.text.lower():
            print_result("Injectable PostGRES detected", payload, "Possible SQL Injection", "1;36")
        elif "ORA" in response.text.lower():
            print_result("Injectable Oracle database detected", payload, "Possible SQL Injection", "1;35")
        else:
            print_result("Not Injectable", payload, "No SQL Injection Detected", "1;31")

    except requests.exceptions.RequestException as e:
        print("\033[1;31mError saat mengakses URL:\033[0m", e)
