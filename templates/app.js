// const faqs = document.querySelectorAll(".faq");

// faqs.forEach(faq => {
//     faq.addEventListener("click",()=>  {
//         faq.classList.toggle("active");
//     })
// })








// const faqs = document.querySelectorAll(".faq");

// faqs.forEach(faq => {
//     faq.addEventListener("click",()=>  {
//         faq.classList.toggle("actve");
//     })
// })



// faq.addEventListener("click", () => {
//         if(!faq.classList.contains("active")){
//         faqs.forEach(faq => {
//             faq.classList.remove('active');
//         })}
//         faq.classList.toggle("active");
//     });

const faqs = document.querySelectorAll(".faq");

faqs.forEach(faq => {
    faq.addEventListener("click", () => {
        if (!faq.classList.contains("active")) {
            faqs.forEach(otherFaq => {
                otherFaq.classList.remove('active');
            });
        }
        faq.classList.toggle("active");
    });
});
