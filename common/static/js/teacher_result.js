document.addEventListener('DOMContentLoaded', async () => {
    const form = document.getElementById('upload-form');
    const resultMessage = document.getElementById('resultMessage') || document.createElement('div');
    const resultContainer = document.getElementById('resultContainer') || document.createElement('div');

    if (!resultMessage.id) {
        resultMessage.id = 'resultMessage';
        form.parentElement.appendChild(resultMessage);
    }

    if (!resultContainer.id) {
        resultContainer.id = 'resultContainer';
        resultContainer.classList.add('mt-4');
        form.parentElement.appendChild(resultContainer);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
            const class_name = document.getElementById('class_name').value;
            const section = document.getElementById('section').value;
            const teacher_name = document.getElementById('teacher_name').value;
            const exam_name = document.getElementById('exam_name').value;
            const subject_name = document.getElementById('subject_name')?.value;

            const params = new URLSearchParams({
                class_name,
                section,
                teacher_name,
                exam_name,
            });

            if (subject_name) params.append('subject_name', subject_name)

            const response = await fetch(`/common/teacher-class-results?${params.toString()}`, {
                method: "GET",
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            console.log("Response data:", data);

            if (!response.ok) {
                resultMessage.innerHTML = `<div class="alert alert-danger">Error: ${data.message || "Failed to fetch results"}</div>`;
                return;
            }

            resultMessage.innerHTML = `<div class="alert alert-success">Results fetched successfully!</div>`;

            if (Array.isArray(data?.data?.students) && data?.data?.students?.length > 0) {
                let tableHTML = `
                    <table class="table table-bordered table-striped mt-3">
                        <thead class="table-dark">
                            <tr>
                                <th>Class Name</th>
                                <th>Section</th>
                                <th>Teacher Name</th>
                                <th>Subject</th>
                                <th>Student Name</th>
                                <th>Obtained Marks</th>
                                <th>Total Marks</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                data?.data?.students.forEach(item => {
                    item?.student_data?.forEach(item1 => {
                        tableHTML += `
                            <tr>
                                <td>${data?.data?.class_name}</td>
                                <td>${data?.data?.section}</td>
                                <td>${data?.data?.teacher_name}</td>
                                <td>${item.subject_name}</td>
                                <td>${item1.student_name}</td>
                                <td>${item1.obtained_marks}</td>
                                <td>${item1.total_marks}</td>
                            </tr>
                        `;
                    });
                });

                tableHTML += `</tbody></table>`;
                resultContainer.innerHTML = tableHTML;
            } else {
                resultContainer.innerHTML = `<div class="alert alert-warning mt-3">No data found for given criteria.</div>`;
            }

        } catch (error) {
            console.error("Error fetching data:", error);
            resultMessage.innerHTML = `<div class="alert alert-danger">Unexpected error occurred.</div>`;
        }
    });
});
