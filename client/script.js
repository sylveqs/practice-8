const API_BASE_URL = 'http://localhost:8000';
let currentView = 'list';

const productsList = document.getElementById('productsList');
const productDetailSection = document.getElementById('productDetailSection');
const productDetail = document.getElementById('productDetail');
const categoriesSection = document.getElementById('categoriesSection');
const categoriesList = document.getElementById('categoriesList');
const statusMessage = document.getElementById('statusMessage');
const serverStatus = document.getElementById('serverStatus');

const loadAllProductsBtn = document.getElementById('loadAllProducts');
const loadProductByIdBtn = document.getElementById('loadProductById');
const loadCategoriesBtn = document.getElementById('loadCategories');
const backToListBtn = document.getElementById('backToList');


async function checkServerConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            serverStatus.textContent = 'Подключен';
            serverStatus.className = 'connected';
            return true;
        }
    } catch (error) {
        console.error('Сервер недоступен:', error);
        serverStatus.textContent = 'Не подключен';
        return false;
    }
}

function showStatus(message, isError = false) {
    statusMessage.textContent = message;
    statusMessage.className = isError ? 'status-message error' : 'status-message';
}
async function loadAllProducts() {
    showStatus('Загрузка товаров...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/products/all`);
        
        if (!response.ok) {
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        
        const products = await response.json();
        displayProducts(products);
        showStatus(`Загружено ${products.length} товаров`);
        
        // Показать список товаров
        showListView();
        
    } catch (error) {
        console.error('Ошибка при загрузке товаров:', error);
        showStatus(`Ошибка: ${error.message}`, true);
    }
}

// Загрузить товар по ID
async function loadProductById() {
    const productId = document.getElementById('productIdInput').value;
    
    if (!productId || productId < 1) {
        showStatus('Введите корректный ID товара', true);
        return;
    }
    
    showStatus(`Поиск товара с ID: ${productId}...`);
    
    try {
        const response = await fetch(`${API_BASE_URL}/products/get/${productId}`);
        
        if (!response.ok) {
            if (response.status === 404) {
                throw new Error('Товар не найден');
            }
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        
        const product = await response.json();
        displayProductDetail(product);
        showStatus(`Товар найден: ${product.name}`);
        
        // Показать детали товара
        showDetailView();
        
    } catch (error) {
        console.error('Ошибка при поиске товара:', error);
        showStatus(`Ошибка: ${error.message}`, true);
    }
}

// Загрузить все категории
async function loadCategories() {
    showStatus('Загрузка категорий...');
    
    try {
        const response = await fetch(`${API_BASE_URL}/categories/all`);
        
        if (!response.ok) {
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        
        const categories = await response.json();
        displayCategories(categories);
        showStatus(`Загружено ${categories.length} категорий`);
        
        // Показать категории
        categoriesSection.style.display = 'block';
        
    } catch (error) {
        console.error('Ошибка при загрузке категорий:', error);
        showStatus(`Ошибка: ${error.message}`, true);
    }
}

// Отобразить товары в виде карточек
function displayProducts(products) {
    if (products.length === 0) {
        productsList.innerHTML = '<div class="loading">Товары не найдены</div>';
        return;
    }
    
    productsList.innerHTML = products.map(product => `
        <div class="product-card" onclick="showProductDetail(${product.id})" style="cursor: pointer;">
            <div class="product-image">
                <i class="fas fa-box"></i>
            </div>
            <div class="product-info">
                <h3 class="product-title">${product.name}</h3>
                <p class="product-description">${product.description || 'Нет описания'}</p>
                <div class="product-price">${product.price.toFixed(2)} ₽</div>
                <div class="product-meta">
                    <span><i class="fas fa-tag"></i> ID: ${product.id}</span>
                    <span><i class="fas fa-layer-group"></i> ${product.stock_quantity} шт.</span>
                    ${product.category ? `<span><i class="fas fa-folder"></i> ${product.category.name}</span>` : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// Отобразить детали товара
function displayProductDetail(product) {
    productDetail.innerHTML = `
        <div class="detail-row">
            <div class="detail-label">Название</div>
            <div class="detail-value">${product.name}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Описание</div>
            <div class="detail-value">${product.description || 'Нет описания'}</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Цена</div>
            <div class="detail-value" style="color: #27ae60; font-weight: 600;">${product.price.toFixed(2)} ₽</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">Количество на складе</div>
            <div class="detail-value">${product.stock_quantity} шт.</div>
        </div>
        <div class="detail-row">
            <div class="detail-label">ID товара</div>
            <div class="detail-value">${product.id}</div>
        </div>
        ${product.category ? `
        <div class="detail-row">
            <div class="detail-label">Категория</div>
            <div class="detail-value">${product.category.name}</div>
        </div>
        ${product.category.description ? `
        <div class="detail-row">
            <div class="detail-label">Описание категории</div>
            <div class="detail-value">${product.category.description}</div>
        </div>
        ` : ''}
        ` : ''}
    `;
}

// Отобразить категории
function displayCategories(categories) {
    if (categories.length === 0) {
        categoriesList.innerHTML = '<div class="loading">Категории не найдены</div>';
        return;
    }
    
    categoriesList.innerHTML = categories.map(category => `
        <div class="category-tag">
            <i class="fas fa-tag"></i> ${category.name}
            ${category.description ? `<br><small>${category.description}</small>` : ''}
        </div>
    `).join('');
}

// Показать детали конкретного товара
async function showProductDetail(productId) {
    showStatus(`Загрузка товара ID: ${productId}...`);
    
    try {
        const response = await fetch(`${API_BASE_URL}/products/get/${productId}`);
        
        if (!response.ok) {
            throw new Error(`HTTP ошибка: ${response.status}`);
        }
        
        const product = await response.json();
        displayProductDetail(product);
        showStatus(`Товар загружен: ${product.name}`);
        
        showDetailView();
        
    } catch (error) {
        console.error('Ошибка при загрузке товара:', error);
        showStatus(`Ошибка: ${error.message}`, true);
    }
}

// Показать список товаров
function showListView() {
    document.querySelector('.products').style.display = 'block';
    productDetailSection.style.display = 'none';
    categoriesSection.style.display = 'none';
    currentView = 'list';
}

// Показать детали товара
function showDetailView() {
    document.querySelector('.products').style.display = 'none';
    productDetailSection.style.display = 'block';
    categoriesSection.style.display = 'none';
    currentView = 'detail';
}

// Инициализация
async function init() {
    // Проверить подключение к серверу
    await checkServerConnection();
    
    // Назначить обработчики событий
    loadAllProductsBtn.addEventListener('click', loadAllProducts);
    loadProductByIdBtn.addEventListener('click', loadProductById);
    loadCategoriesBtn.addEventListener('click', loadCategories);
    backToListBtn.addEventListener('click', showListView);
    
    // Загрузить товары при загрузке страницы
    await loadAllProducts();
    
    showStatus('Система готова к работе. Загружены все товары.');
}

// Запуск приложения
document.addEventListener('DOMContentLoaded', init);