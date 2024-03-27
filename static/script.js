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
            <td><input type="text" name="description[]"></td>
            <td><input type="number" name="quantity[]"></td>
            <td><input type="number" name="price[]"></td>
            <td><input type="number" name="tax[]"></td>
            <td><input type="number" name="amount[]" readonly></td>
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
    html2canvas(document.body).then(function(canvas) {
        var imgData = canvas.toDataURL('image/png');
        var pdf = new jsPDF();
        pdf.addImage(imgData, 'PNG', 0, 0);
        var pdfData = pdf.output('blob');
        
        // Send the captured image and PDF data to the server
        var formData = new FormData();
        formData.append('imageData', imgData);
        formData.append('pdfData', pdfData);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/billing', true);
        xhr.onload = function() {
            if (xhr.status == 200) {
                // Redirect or handle confirmation
            } else {
                // Handle error
            }
        };
        xhr.send(formData);
    });
}
// fetch invoice data
function fetchInvoiceData() {
    fetch('/myfiles')
        .then(response => response.json())
        .then(data => {
            // Clear previous content
            document.getElementById('invoiceDetails').innerHTML = '';

            // Loop through the fetched data and create HTML elements to display it
            data.forEach(invoice => {
                const invoiceDiv = document.createElement('div');
                invoiceDiv.innerHTML = `<p>Invoice ID: ${invoice[0]}</p>`; // Adjust this according to your table structure
                document.getElementById('invoiceDetails').appendChild(invoiceDiv);
            });
        })
        .catch(error => console.error('Error fetching invoice data:', error));
}

