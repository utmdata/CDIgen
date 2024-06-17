const div1 = document.getElementById("div1");
const div2 = document.getElementById("div2");

const lista_total = Sortable.create(div1, {
   group: {
      name: "lista_total"
   }, 
   animation: 150,  
});

const lista_cdi = Sortable.create(div2, {
    group: {
       name: "lista_total"
    }, 
    animation: 150, 
    store:{
        set:function(sortable){
            const orden = sortable.toArray();
            console.log(orden);
            console.log(orden.join(","));
            localStorage.setItem("tareas_cdi", orden.join(","));
            
            // Enviar datos al servidor cuando se actualiza localStorage http://datahub.utm.csic.es/cdigen/guardar_tareas
            fetch('http://161.111.137.92:8001/guardar_tareas', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ tareas_cdi: orden.join(",") }),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Respuesta del servidor:', data);
            })
            .catch(error => {
                console.error('Error al enviar las tareas:', error);
            });
        } 
    } 
});
