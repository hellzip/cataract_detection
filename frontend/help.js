// FAQ Toggle Logic
document.querySelectorAll('.faq-question').forEach(button => {
    button.addEventListener('click', () => {
        const answer = button.nextElementSibling;

        // Toggle display of the answer
        answer.style.display = answer.style.display === 'block' ? 'none' : 'block';
    });
});
