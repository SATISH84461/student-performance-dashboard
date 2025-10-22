document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('upload-form');
    const resultMessage = document.getElementById('resultMessage') || document.createElement('div');
    if (!resultMessage.id) {
        resultMessage.id = 'resultMessage';
        form.parentElement.appendChild(resultMessage);
    }
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        console.log(formData);
        try {
            const response = await fetch("/common/convert-file", {
                method: "POST",
                body: formData
            });

            const data = await response.json();
            if (!response.ok) {
                resultMessage.innerHTML = `<div class="alert alert-danger">Error: ${data.message || "Upload failed"}</div>`;
                return;
            }
            const uploadData = {
                teacher_name: document.getElementById('teacher_name').value,
                class_name: document.getElementById('class_name').value,
                section: document.getElementById('section').value,
                exam_name: document.getElementById('exam_name').value,
                subject_name: document.getElementById('subject_name').value,
                total_marks: parseInt(document.getElementById('total_marks').value),
                passing_marks: parseInt(document.getElementById('passing_marks').value),
                data: data?.data
            };
            console.log("Server response:", uploadData);
            const uploadResponse = await fetch("/common/performance2", {
                method: "POST",
                body: JSON.stringify(uploadData),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });
            const uploadResponseData = await uploadResponse.json();
            if (!uploadResponse.ok) {
                resultMessage.innerHTML = `<div class="alert alert-danger">Error: ${uploadResponseData.message || "Upload failed"}</div>`;
                return;
            }
            resultMessage.innerHTML = `<div class="alert alert-success">${uploadResponseData.message}</div>`;
            form.reset();

        } catch (error) {
            console.error("Upload failed:", error);
            resultMessage.innerHTML = `<div class="alert alert-danger">Unexpected error occurred</div>`;
        }
    });
});
