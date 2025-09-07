document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generateBtn');
    const loading = document.getElementById('loading');
    const snowflakeImage = document.getElementById('snowflakeImage');
    
    generateBtn.addEventListener('click', function() {
        // Mostrar carga
        loading.classList.remove('hidden');
        snowflakeImage.classList.add('hidden');
        
        // Hacer solicitud al servidor
        fetch('/generate_snowflake')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Mostrar la imagen
                snowflakeImage.src = 'data:image/png;base64,' + data.image;
                snowflakeImage.classList.remove('hidden');
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al generar el copo de nieve: ' + error.message);
            })
            .finally(() => {
                // Ocultar carga
                loading.classList.add('hidden');
            });
    });
});