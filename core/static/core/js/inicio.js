// Función para abrir el modal del mapa
function openMapModal() {
    document.getElementById("mapModal").style.display = "block";
}

// Función para cerrar el modal del mapa
function closeMapModal() {
    document.getElementById("mapModal").style.display = "none";
}

// Función para abrir el modal de suscripción
function openSubscriptionModal() {
    document.getElementById("subscriptionModal").style.display = "block";
}

// Función para cerrar el modal de suscripción
function closeSubscriptionModal() {
    document.getElementById("subscriptionModal").style.display = "none";
}

// Cerrar el modal si se hace clic fuera del contenido del modal
window.onclick = function(event) {
    var mapModal = document.getElementById("mapModal");
    var subscriptionModal = document.getElementById("subscriptionModal");

    if (event.target == mapModal) {
        mapModal.style.display = "none";
    }

    if (event.target == subscriptionModal) {
        subscriptionModal.style.display = "none";
    }
}

