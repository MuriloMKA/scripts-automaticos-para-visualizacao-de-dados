"""
Mock SAP OData data generator for demonstration and testing.

This module provides realistic sample data for SAP entities (Materials, Sales Orders, Invoices)
that mimics the structure of real SAP OData responses. Used when SAP_ODATA_BASE_URL is not configured.
"""

from typing import Any


def get_mock_materials(top: int = 50) -> list[dict[str, Any]]:
    """
    Generate mock SAP Material Master records.
    
    Args:
        top: Number of materials to return (default 50, max will be capped to actual list size)
    
    Returns:
        List of material dictionaries with SAP-like properties
    """
    materials = [
        {
            "Material": "MAT-001",
            "MaterialType": "FERT",
            "MaterialDescription": "Kraft Paper Roll 80gsm",
            "UnitOfMeasure": "KG",
            "NetPrice": "2.45",
            "Currency": "BRL",
            "Plant": "P001",
            "StorageLocation": "SL01",
            "QuantityOnHand": "15000",
        },
        {
            "Material": "MAT-002",
            "MaterialType": "FERT",
            "MaterialDescription": "Kraft Paper Roll 100gsm",
            "UnitOfMeasure": "KG",
            "NetPrice": "3.20",
            "Currency": "BRL",
            "Plant": "P001",
            "StorageLocation": "SL01",
            "QuantityOnHand": "12500",
        },
        {
            "Material": "MAT-003",
            "MaterialType": "FERT",
            "MaterialDescription": "Corrugated Cardboard Sheet",
            "UnitOfMeasure": "M2",
            "NetPrice": "5.75",
            "Currency": "BRL",
            "Plant": "P001",
            "StorageLocation": "SL02",
            "QuantityOnHand": "8200",
        },
        {
            "Material": "MAT-004",
            "MaterialType": "FERT",
            "MaterialDescription": "Laminated Packaging Film",
            "UnitOfMeasure": "M",
            "NetPrice": "12.50",
            "Currency": "BRL",
            "Plant": "P002",
            "StorageLocation": "SL01",
            "QuantityOnHand": "5600",
        },
        {
            "Material": "MAT-005",
            "MaterialType": "FERT",
            "MaterialDescription": "Adhesive Label Rolls",
            "UnitOfMeasure": "ROLL",
            "NetPrice": "18.90",
            "Currency": "BRL",
            "Plant": "P002",
            "StorageLocation": "SL03",
            "QuantityOnHand": "3200",
        },
        {
            "Material": "MAT-006",
            "MaterialType": "ROH",
            "MaterialDescription": "Pulp Fiber (Raw Material)",
            "UnitOfMeasure": "TON",
            "NetPrice": "450.00",
            "Currency": "BRL",
            "Plant": "P001",
            "StorageLocation": "RM01",
            "QuantityOnHand": "250",
        },
        {
            "Material": "MAT-007",
            "MaterialType": "FERT",
            "MaterialDescription": "Protective Wrap 50mm",
            "UnitOfMeasure": "M",
            "NetPrice": "3.45",
            "Currency": "BRL",
            "Plant": "P002",
            "StorageLocation": "SL02",
            "QuantityOnHand": "9800",
        },
        {
            "Material": "MAT-008",
            "MaterialType": "FERT",
            "MaterialDescription": "Printed Carton Box (Large)",
            "UnitOfMeasure": "UNIT",
            "NetPrice": "8.20",
            "Currency": "BRL",
            "Plant": "P001",
            "StorageLocation": "SL04",
            "QuantityOnHand": "4500",
        },
        {
            "Material": "MAT-009",
            "MaterialType": "FERT",
            "MaterialDescription": "Tissue Paper Roll",
            "UnitOfMeasure": "KG",
            "NetPrice": "4.10",
            "Currency": "BRL",
            "Plant": "P002",
            "StorageLocation": "SL01",
            "QuantityOnHand": "7200",
        },
        {
            "Material": "MAT-010",
            "MaterialType": "VERP",
            "MaterialDescription": "Packaging Components Kit",
            "UnitOfMeasure": "UNIT",
            "NetPrice": "25.50",
            "Currency": "BRL",
            "Plant": "P001",
            "StorageLocation": "SL05",
            "QuantityOnHand": "1200",
        },
    ]
    return materials[:top]


def get_mock_sales_orders(top: int = 50) -> list[dict[str, Any]]:
    """
    Generate mock SAP Sales Order records.
    
    Args:
        top: Number of orders to return (default 50, max will be capped to actual list size)
    
    Returns:
        List of sales order dictionaries with SAP-like properties
    """
    orders = [
        {
            "SalesOrder": "SO-000001",
            "OrderDate": "2025-11-01",
            "Customer": "CUST-100",
            "CustomerName": "ABC Packaging Industries",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "C",
            "OrderStatusText": "Completed",
            "OrderValue": "45000.00",
            "Currency": "BRL",
            "Plant": "P001",
            "DeliveryDate": "2025-11-15",
            "LineItems": 4,
        },
        {
            "SalesOrder": "SO-000002",
            "OrderDate": "2025-11-02",
            "Customer": "CUST-200",
            "CustomerName": "XYZ Manufacturing Ltd",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "D",
            "OrderStatusText": "Delivered",
            "OrderValue": "62500.00",
            "Currency": "BRL",
            "Plant": "P002",
            "DeliveryDate": "2025-11-18",
            "LineItems": 5,
        },
        {
            "SalesOrder": "SO-000003",
            "OrderDate": "2025-11-03",
            "Customer": "CUST-150",
            "CustomerName": "Global Logistics Corp",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "A",
            "OrderStatusText": "Active",
            "OrderValue": "38750.00",
            "Currency": "BRL",
            "Plant": "P001",
            "DeliveryDate": "2025-11-20",
            "LineItems": 3,
        },
        {
            "SalesOrder": "SO-000004",
            "OrderDate": "2025-11-04",
            "Customer": "CUST-300",
            "CustomerName": "Regional Distribution Center",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "C",
            "OrderStatusText": "Completed",
            "OrderValue": "51200.00",
            "Currency": "BRL",
            "Plant": "P002",
            "DeliveryDate": "2025-11-22",
            "LineItems": 6,
        },
        {
            "SalesOrder": "SO-000005",
            "OrderDate": "2025-11-05",
            "Customer": "CUST-250",
            "CustomerName": "Metro Retail Group",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "A",
            "OrderStatusText": "Active",
            "OrderValue": "29500.00",
            "Currency": "BRL",
            "Plant": "P001",
            "DeliveryDate": "2025-11-25",
            "LineItems": 4,
        },
        {
            "SalesOrder": "SO-000006",
            "OrderDate": "2025-11-06",
            "Customer": "CUST-100",
            "CustomerName": "ABC Packaging Industries",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "D",
            "OrderStatusText": "Delivered",
            "OrderValue": "55800.00",
            "Currency": "BRL",
            "Plant": "P002",
            "DeliveryDate": "2025-11-28",
            "LineItems": 5,
        },
        {
            "SalesOrder": "SO-000007",
            "OrderDate": "2025-11-07",
            "Customer": "CUST-350",
            "CustomerName": "Premium Export Services",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "C",
            "OrderStatusText": "Completed",
            "OrderValue": "72300.00",
            "Currency": "BRL",
            "Plant": "P001",
            "DeliveryDate": "2025-12-01",
            "LineItems": 7,
        },
        {
            "SalesOrder": "SO-000008",
            "OrderDate": "2025-11-08",
            "Customer": "CUST-200",
            "CustomerName": "XYZ Manufacturing Ltd",
            "SalesOrganization": "SO1000",
            "DistributionChannel": "10",
            "Division": "00",
            "OrderStatus": "A",
            "OrderStatusText": "Active",
            "OrderValue": "44100.00",
            "Currency": "BRL",
            "Plant": "P001",
            "DeliveryDate": "2025-12-03",
            "LineItems": 4,
        },
    ]
    return orders[:top]


def get_mock_invoices(top: int = 50) -> list[dict[str, Any]]:
    """
    Generate mock SAP Invoice records.
    
    Args:
        top: Number of invoices to return (default 50, max will be capped to actual list size)
    
    Returns:
        List of invoice dictionaries with SAP-like properties
    """
    invoices = [
        {
            "Invoice": "INV-2025-00001",
            "InvoiceDate": "2025-11-15",
            "SalesOrder": "SO-000001",
            "Customer": "CUST-100",
            "CustomerName": "ABC Packaging Industries",
            "InvoiceStatus": "P",
            "InvoiceStatusText": "Posted",
            "GrossAmount": "48500.00",
            "TaxAmount": "3500.00",
            "NetAmount": "45000.00",
            "Currency": "BRL",
            "DueDate": "2025-12-15",
            "PaymentStatus": "O",
            "PaymentStatusText": "Open",
        },
        {
            "Invoice": "INV-2025-00002",
            "InvoiceDate": "2025-11-18",
            "SalesOrder": "SO-000002",
            "Customer": "CUST-200",
            "CustomerName": "XYZ Manufacturing Ltd",
            "InvoiceStatus": "P",
            "InvoiceStatusText": "Posted",
            "GrossAmount": "67500.00",
            "TaxAmount": "5000.00",
            "NetAmount": "62500.00",
            "Currency": "BRL",
            "DueDate": "2025-12-18",
            "PaymentStatus": "C",
            "PaymentStatusText": "Cleared",
        },
        {
            "Invoice": "INV-2025-00003",
            "InvoiceDate": "2025-11-20",
            "SalesOrder": "SO-000003",
            "Customer": "CUST-150",
            "CustomerName": "Global Logistics Corp",
            "InvoiceStatus": "P",
            "InvoiceStatusText": "Posted",
            "GrossAmount": "41800.00",
            "TaxAmount": "3050.00",
            "NetAmount": "38750.00",
            "Currency": "BRL",
            "DueDate": "2025-12-20",
            "PaymentStatus": "O",
            "PaymentStatusText": "Open",
        },
        {
            "Invoice": "INV-2025-00004",
            "InvoiceDate": "2025-11-22",
            "SalesOrder": "SO-000004",
            "Customer": "CUST-300",
            "CustomerName": "Regional Distribution Center",
            "InvoiceStatus": "P",
            "InvoiceStatusText": "Posted",
            "GrossAmount": "55200.00",
            "TaxAmount": "4000.00",
            "NetAmount": "51200.00",
            "Currency": "BRL",
            "DueDate": "2025-12-22",
            "PaymentStatus": "C",
            "PaymentStatusText": "Cleared",
        },
        {
            "Invoice": "INV-2025-00005",
            "InvoiceDate": "2025-11-25",
            "SalesOrder": "SO-000005",
            "Customer": "CUST-250",
            "CustomerName": "Metro Retail Group",
            "InvoiceStatus": "P",
            "InvoiceStatusText": "Posted",
            "GrossAmount": "31800.00",
            "TaxAmount": "2300.00",
            "NetAmount": "29500.00",
            "Currency": "BRL",
            "DueDate": "2025-12-25",
            "PaymentStatus": "O",
            "PaymentStatusText": "Open",
        },
    ]
    return invoices[:top]


def get_mock_odata_response(
    entity_path: str, top: int = 50, select: list[str] | None = None
) -> dict[str, Any]:
    """
    Generate a mock OData response in SAP format.
    
    Supports entities:
    - Materials (entity_path: 'Materials' or 'C_Material')
    - SalesOrders (entity_path: 'SalesOrders' or 'C_SalesOrder')
    - Invoices (entity_path: 'Invoices' or 'C_Invoice')
    
    Args:
        entity_path: The OData entity name/path (e.g., 'Materials', 'SalesOrders', 'Invoices')
        top: Maximum number of records to return
        select: List of field names to include (optional; returns all if None)
    
    Returns:
        Dictionary in SAP OData response format with 'd.results' structure
    """
    entity_key = entity_path.strip("/").lower()
    
    # Map entity paths to mock data generators
    if "material" in entity_key:
        rows = get_mock_materials(top)
    elif "salesorder" in entity_key or "sales_order" in entity_key:
        rows = get_mock_sales_orders(top)
    elif "invoice" in entity_key:
        rows = get_mock_invoices(top)
    else:
        rows = []
    
    # Apply field selection if specified
    if select and rows:
        rows = [
            {key: row.get(key) for key in select if key in row}
            for row in rows
        ]
    
    return {
        "d": {
            "results": rows,
            "__count": str(len(rows)),
        }
    }
