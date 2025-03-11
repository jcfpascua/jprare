document.addEventListener("DOMContentLoaded", function () {

    // Load data for Supplier
    fetch("http://localhost:8080/version1/api/supplier.php")
        .then(response => response.json())
        .then(data => {
            const supplierList = document.getElementById("supplierList");
            supplierList.innerHTML = ""; // Clear existing list
            data.forEach(supplier => {
                const listItem = document.createElement("li");
                listItem.textContent = `${supplier.name} - ${supplier.contact}`;
                supplierList.appendChild(listItem);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Merchant
    fetch("http://localhost:8080/version1/api/merchant.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("merchantTableBody");
            data.forEach(merchant => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${merchant.merchantID}</td>
                    <td>${merchant.merchant_name}</td>
                    <td>${merchant.addressID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Address
    fetch("http://localhost:8080/version1/api/address.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("addressTableBody");
            data.forEach(address => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${address.addressID}</td>
                    <td>${address.description}</td>
                    <td>${address.streetID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Barangay
    fetch("http://localhost:8080/version1/api/barangay.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("barangayTableBody");
            data.forEach(barangay => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${barangay.barangayID}</td>
                    <td>${barangay.barangayName}</td>
                    <td>${barangay.cityID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for City
    fetch("http://localhost:8080/version1/api/city.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("cityTableBody");
            data.forEach(city => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${city.cityID}</td>
                    <td>${city.cityName}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Contact Details
    fetch("http://localhost:8080/version1/api/contact_details.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("contactDetailsTableBody");
            data.forEach(contactDetail => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${contactDetail.contact_detailsID}</td>
                    <td>${contactDetail.customerID}</td>
                    <td>${contactDetail.contact_typeID}</td>
                    <td>${contactDetail.value}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Contact Types
    fetch("http://localhost:8080/version1/api/contact_type.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("contactTypeTableBody");
            data.forEach(contactType => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${contactType.contact_typeID}</td>
                    <td>${contactType.value}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Customer Order Details
    fetch("http://localhost:8080/version1/api/customer_order_details.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("customerOrderDetailsTableBody");
            data.forEach(detail => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${detail.customer_order_detailsID}</td>
                    <td>${detail.customer_orderID}</td>
                    <td>${detail.itemID}</td>
                    <td>${detail.quantity}</td>
                    <td>${detail.total}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Customer Orders
    fetch("http://localhost:8080/version1/api/customer_order.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("customerOrderTableBody");
            data.forEach(order => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${order.customer_orderID}</td>
                    <td>${order.customerID}</td>
                    <td>${order.order_date}</td>
                    <td>${order.merchantID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Customers
    fetch("http://localhost:8080/version1/api/customers.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("customerTableBody");
            data.forEach(customer => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${customer.customerID}</td>
                    <td>${customer.customer_name}</td>
                    <td>${customer.addressID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Expense Details
    fetch("http://localhost:8080/version1/api/expense_details.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("expenseDetailsTableBody");
            data.forEach(detail => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${detail.expense_detailsID}</td>
                    <td>${detail.expenseID}</td>
                    <td>${detail.expense_typeID}</td>
                    <td>${detail.amount}</td>
                    <td>${detail.quantity}</td>
                    <td>${detail.subtotal}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Expenses
    fetch("http://localhost:8080/version1/api/expense.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("expenseTableBody");
            data.forEach(expense => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${expense.expenseID}</td>
                    <td>${expense.expense_date}</td>
                    <td>${expense.total}</td>
                    <td>${expense.merchantID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Expense Types
    fetch("http://localhost:8080/version1/api/expense_type.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("expenseTypeTableBody");
            data.forEach(type => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${type.expense_typeID}</td>
                    <td>${type.title}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Inventory
    fetch("http://localhost:8080/version1/api/item.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("inventoryTableBody");
            data.forEach(item => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${item.itemID}</td>
                    <td>${item.item_name}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Merchant Order Details
    fetch("http://localhost:8080/version1/api/merchant_order_details.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("merchantOrderDetailsTableBody");
            data.forEach(detail => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${detail.merchant_order_detailsID}</td>
                    <td>${detail.merchant_orderID}</td>
                    <td>${detail.customer_order_detailsID}</td>
                    <td>${detail.quantity}</td>
                    <td>${detail.details}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Merchant Orders
    fetch("http://localhost:8080/version1/api/merchant_order.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("merchantOrderTableBody");
            data.forEach(order => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${order.merchant_orderID}</td>
                    <td>${order.merchantID}</td>
                    <td>${order.merchant_name}</td>
                    <td>${order.supplierID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

    // Load data for Street
    fetch("http://localhost:8080/version1/api/street.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("streetTableBody");
            data.forEach(street => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${street.streetID}</td>
                    <td>${street.streetName}</td>
                    <td>${street.barangayID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error));

        fetch("http://localhost:8080/version1/api/supplier.php")
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("supplierTableBody");
            data.forEach(supplier => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${supplier.supplierID}</td>
                    <td>${supplier.supplier_name}</td>
                    <td>${supplier.addressID}</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error("Error fetching data:", error))
});