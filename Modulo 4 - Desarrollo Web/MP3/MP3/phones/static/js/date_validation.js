document.addEventListener("DOMContentLoaded", function (event) {
  if(window.location.pathname === '/phones/smartphones/create/'){
    const phoneForm = document.getElementById('phone-form');
    if (phoneForm) {
      const releaseDateInput = phoneForm.querySelector("#id_release_date");
      const submitBtn = phoneForm.querySelector('input[type="submit"]');
      if (releaseDateInput && submitBtn) {
        const todayDt = new Date();
        // Primer Check usando la facha maxima admitida por el input
        releaseDateInput.max = formatDateToString(todayDt);
        releaseDateInput.addEventListener('change', e => {
          let pickedDate = new Date(e.target.value.split("-"));
          // Segundo Check comparando la fecha escogida con la fecha de hoy
          if (pickedDate > todayDt){
            alert(`La fecha seleccionada no puede ser mayor a ${formatDateToString(todayDt)}`)
            //Desabilitar Submit
            submitBtn.setAttribute('disabled', "true");
          }else{
            //Habilitar Submit
            submitBtn.removeAttribute('disabled'); 
          }
        })
      }
    }
  }
});

function formatDateToString(date){
  let dd = (date.getDate() < 10 ? '0' : '') + date.getDate();
  let MM = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);
  let yyyy = date.getFullYear();
  return (yyyy + "-" + MM + "-" + dd);
}