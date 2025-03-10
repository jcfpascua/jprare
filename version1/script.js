document.addEventListener("DOMContentLoaded", function () {
    

    const addRecordBtn = document.getElementById("addRecordBtn");
    const tableHeaders = document.getElementById("tableHeaders");
    const tableBody = document.getElementById("tableBody");
    const modal = document.getElementById("formModal");
    const formTitle = document.getElementById("formTitle");
    const formFields = document.getElementById("formFields");
    const dataForm = document.getElementById("dataForm");

    let selectedTable = "customers"; // Default tab

    function loadTableData() {
        console.log(`Fetching data for table: ${selectedTable}`);
        fetch(`http://localhost:8080/version1/api/${selectedTable}.php`)
            .then(response => response.json())
            .then(data => {
                tableHeaders.innerHTML = "";
                tableBody.innerHTML = "";

                if (data.length > 0) {
                    const headers = Object.keys(data[0]);

                    headers.forEach(header => {
                        let th = document.createElement("th");
                        switch (header) {
                            case 'customer_name':
                                th.textContent = 'Customer Name';
                                break;
                            case 'order_date':
                                th.textContent = 'Order Date';
                                break;
                            case 'total_amount':
                                th.textContent = 'Total Amount';
                                break;
                            case 'order_status':
                                th.textContent = 'Order Status';
                                break;
                            case 'supplier_name':
                                th.textContent = 'Supplier Name';
                                break;
                            case 'customer_id':
                                th.textContent = 'Customer ID';
                                break;
                            case 'order_id':
                                th.textContent = 'Order ID';
                                break;
                            case 'supplier_id':
                                th.textContent = 'Supplier ID';
                                break;
                            case 'merchant_id':
                                th.textContent = 'Merchant ID';
                                break;
                            case 'expense_type_id':
                                th.textContent = 'Expense Type ID';
                                break;
                            case 'expense_id':
                                th.textContent = 'Expense ID';
                                break;
                            default:
                                th.textContent = header.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
                        }
                        tableHeaders.appendChild(th);
                    });

                    let actionsTh = document.createElement("th");
                    actionsTh.textContent = "Actions";
                    tableHeaders.appendChild(actionsTh);

                    data.forEach(record => {
                        let tr = document.createElement("tr");

                        headers.forEach(header => {
                            let td = document.createElement("td");
                            td.textContent = record[header];
                            tr.appendChild(td);
                        });

                        let actionTd = document.createElement("td");
                        actionTd.innerHTML = `
                            <button onclick="editRecord(${record[headers[0]]})">Edit</button>
                            <button onclick="deleteRecord(${record[headers[0]]})">Delete</button>
                        `;
                        tr.appendChild(actionTd);
                        tableBody.appendChild(tr);
                    });
                } else {
                    tableBody.innerHTML = "<tr><td colspan='100%'>No data found</td></tr>";
                }
            })
            .catch(error => console.error("Error fetching data:", error));
    }

    function openForm(editMode = false, record = {}) {
        modal.style.display = "block";
        formFields.innerHTML = "";
        formTitle.textContent = editMode ? "Edit Record" : "Add Record";

        fetch(`http://localhost:8080/version1/api/${selectedTable}.php`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    Object.keys(data[0]).forEach(key => {
                        if (key !== `${selectedTable}ID`) {
                            let div = document.createElement("div");
                            div.innerHTML = `<label>${key}:</label> <input type="text" name="${key}" value="${record[key] || ""}">`;
                            formFields.appendChild(div);
                        }
                    });

                    let hiddenID = document.createElement("input");
                    hiddenID.type = "hidden";
                    hiddenID.name = `${selectedTable}ID`;
                    hiddenID.value = record[`${selectedTable}ID`] || "";
                    formFields.appendChild(hiddenID);
                }
            });
    }

    dataForm.addEventListener("submit", function (e) {
        e.preventDefault();
        let formData = new FormData(dataForm);
        let jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        let method = jsonData[`${selectedTable}ID`] ? "PUT" : "POST";

        fetch(`http://localhost:8080/version1/api/${selectedTable}.php`, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData),
        }).then(() => {
            modal.style.display = "none";
            loadTableData();
        });
    });

    window.editRecord = function (id) {
        fetch(`http://localhost:8080/version1/api/${selectedTable}.php?id=${id}`)
            .then(response => response.json())
            .then(data => openForm(true, data[0]));
    };

    window.deleteRecord = function (id) {
        fetch(`http://localhost:8080/version1/api/${selectedTable}.php?id=${id}`, {
            method: "DELETE"
        }).then(() => loadTableData());
    };

    window.openTable = function (evt, tableName) {
        selectedTable = tableName;
        document.querySelectorAll(".tablinks").forEach(tab => tab.classList.remove("active"));
        evt.currentTarget.classList.add("active");
        loadTableData();
    };

    document.querySelector(".close").addEventListener("click", () => modal.style.display = "none");
    addRecordBtn.addEventListener("click", () => openForm());

    // Adding smooth transitions to buttons and forms
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.style.transition = 'background-color 0.3s ease, transform 0.2s ease';
        button.addEventListener('mouseover', () => {
            button.style.backgroundColor = '#0056b3'; // Change to a darker shade on hover
            button.style.transform = 'scale(1.05)'; // Slightly enlarge button
        });
        button.addEventListener('mouseout', () => {
            button.style.backgroundColor = ''; // Reset to original color
            button.style.transform = 'scale(1)'; // Reset size
        });
    });

    // Adding fade-in effect for forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.style.opacity = '0';
        form.style.transition = 'opacity 0.5s ease';
        window.addEventListener('load', () => {
            form.style.opacity = '1'; // Fade in effect on load
        });
    });

    loadTableData();
});
