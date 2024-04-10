//to generate a 6 digit random code
window.onload = function() {
    // Function to generate random 6-digit code
    function generateRandomCode() {
        return Math.floor(100000 + Math.random() * 900000);
    }

    // Generate and display the random code
    var randomCode = generateRandomCode();
    document.getElementById('random-code').textContent = randomCode;
};

//get the element you want to take action once clicked
document.getElementById('btn').addEventListener('click', addFields);

    function addFields() {
        var tableBody = document.getElementById('tableBody');
        var rowCount = tableBody.rows.length + 1;
        var row = tableBody.insertRow();
        row.innerHTML = `
            <td>${rowCount}</td>
            <td><input type="text" class="form-control" name="description[]"></td>
            <td><input type="number" class="form-control" name="quantity[]"></td>
            <td><input type="number" class="form-control" name="price[]"></td>
            <td><input type="number" class="form-control" name="tax[]"></td>
            <td><input type="number" class="form-control" name="amount[]"></td>
            <td><button type="button" onclick="deleteRow(this)" class="btn btn-danger">Delete</button></td>
        `;
    }

    function deleteRow(btn) {
        var row = btn.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }

    document.getElementById('tableBody').addEventListener('input', updateTotal);

    function updateTotal() {
        var total = 0;
        var amounts = document.getElementsByName('amount[]');
        for (var i = 0; i < amounts.length; i++) {
            total += parseFloat(amounts[i].value) || 0;
        }
        document.getElementById('total').textContent = total.toFixed(2);
    }

//capture and save data
function captureAndSave() {
    html2canvas(document.getElementById('surround')).then(function(canvas) {
        var imgData = canvas.toDataURL('image/png');
        
        // Send the captured image data to the server
        var formData = new FormData();
        formData.append('imageData', imgData);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/billing', true);
        xhr.onload = function() {
            if (xhr.status == 200) {
                // After successful creation, fetch updated invoice data
                fetchInvoiceData();
                // Show success message
                alert("Image file has been created successfully");
            } else {
                // Handle error
                alert("Error creating image file");
            }
        };
        xhr.send(formData);
    });
}



// Fetch invoice data when the "My Files" link is clicked
function fetchInvoiceData() {
    fetch('/myfiles')
        .then(response => response.json())
        .then(data => {
            const invoiceDetails = document.getElementById('invoiceDetails');
            invoiceDetails.innerHTML = '';

            data.forEach(invoice => {
                const invoiceDiv = document.createElement('div');
                invoiceDiv.innerHTML = `
                    <p>Invoice ID: ${invoice.id}</p>
                    <p>Company Name: ${invoice.companyName}</p>
                    <!-- Add other fields as needed -->
                `;
                invoiceDetails.appendChild(invoiceDiv);
            });

            // Show the offcanvas after fetching data
            var offcanvasElement = document.getElementById('offcanvasExample');
            var offcanvas = bootstrap.Offcanvas.getInstance(offcanvasElement);
            offcanvas.show();
        })
        .catch(error => {
            console.error('Error fetching invoice data:', error);
            alert('Error fetching invoice data');
        });
}
