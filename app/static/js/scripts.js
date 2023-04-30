// Fetch data from Flask route
function generateReport(classId, subjectId) {

    let url = '/class_report?'

    if (classId) url += `class_id=${classId}&`
    if (subjectId && subjectId !== 'all') url += `subject_id=${subjectId}`
    
    if (window.chart != undefined) {
        window.chart.destroy();
    }

    document.getElementById('reportTable').innerHTML = '';

    fetch(url)
.then(response => response.json())
        .then(data => {
        
            const subjects = data.subjects;
            
            const classes = data.classes;

            // Populate the class dropdown
            const classDropdown = document.getElementById('class-dropdown');
            classDropdown.innerHTML = '';
            classes.forEach(classItem => {
                const option = document.createElement('option');
                // if selected_class_id is not null and selected_class_id is equal to classItem._id
                if (data.selected_class_id && data.selected_class_id == classItem._id) {
                    option.selected = true;
                }
                option.value = classItem._id;
                option.text = classItem.name;
                classDropdown.appendChild(option);
            });

            // Populate the subject dropdown
            const subjectDropdown = document.getElementById('subject-dropdown');
            subjectDropdown.innerHTML = '';

            const option = document.createElement('option');
                option.value = 'all';
                option.text = 'All';
                subjectDropdown.appendChild(option);

            subjects.forEach(subject => {   
                const option = document.createElement('option');
                // if selected_subject_id is not null and selected_subject_id is equal to subject._id
                if (data.selected_subject_id && data.selected_subject_id == subject._id) {
                    option.selected = true;
                }
                option.value = subject._id;
                option.text = subject.name;
                subjectDropdown.appendChild(option);
            });

            if (data.report_type == 'subject') {
            
                // show data from report in table
                const tableBody = document.getElementById('reportTable');
                tableBody.innerHTML = '';
                // add table header
                const tableHeader = document.createElement('tr');
                const subjectNameHeader = document.createElement('th');
                subjectNameHeader.innerText = 'Grades';
                const studentsAppearedHeader = document.createElement('th');
                studentsAppearedHeader.innerText = 'Students';
                const passPercentageHeader = document.createElement('th');
                passPercentageHeader.innerText = 'Pass';

                tableHeader.appendChild(subjectNameHeader);
                tableHeader.appendChild(studentsAppearedHeader);
                tableHeader.appendChild(passPercentageHeader);
                tableBody.appendChild(tableHeader);
                // add table rows
                
                data.report.forEach(item => {
                    const row = document.createElement('tr');
                    const grade = document.createElement('td');
                    grade.innerText = item.grade;
                    const studentsAppeared = document.createElement('td');
                    studentsAppeared.innerText = item.students;
                    
                    const passPercentage = document.createElement('td');
                    passPercentage.innerText = item.percentage;
                    row.appendChild(grade);
                    row.appendChild(studentsAppeared);
                    row.appendChild(passPercentage);
                    tableBody.appendChild(row);
                });
            
            const grades = [];
            const percentages = [];
            const colors = ['green', 'blue', 'yellow', 'orange', 'red'];

            // Extract data from response
            const report = data.report;
            report.forEach(item => {
                grades.push(item.grade);
                percentages.push(item.percentage);
            });

            // Create pie chart
            // Destroy the existing chart with ID '0'
            if (window.chart != undefined) {
                window.chart.destroy();
            }
            const ctx = document.getElementById('myChart').getContext('2d');
            window.chart = new Chart(ctx, {
                type: 'pie',
                data: {
                labels: grades,
                datasets: [{
                    data: percentages,
                    backgroundColor: colors
                }]
                },
                options: {
                responsive: false,
                title: {
                    display: true,
                    text: `Grade Wise Report - Class: ${data.class_name}, Subject: ${data.subject_name}`
                }
                }
            });
        } else {
            // Extract the data for the chart
            const labels = data.report.map(subject => subject.subject_name);
                const passPercentages = data.report.map(subject => subject.pass_percentage);
                
                // show report in table
                const tableBody = document.getElementById('reportTable');
                tableBody.innerHTML = '';
                // add table header
                const tableHeader = document.createElement('tr');
                const subjectNameHeader = document.createElement('th');
                subjectNameHeader.innerText = 'Subject';
                const passPercentageHeader = document.createElement('th');
                passPercentageHeader.innerText = 'Pass';
                const studentsAppearedHeader = document.createElement('th');
                studentsAppearedHeader.innerText = 'Students';

                tableHeader.appendChild(subjectNameHeader);
                tableHeader.appendChild(passPercentageHeader);
                tableHeader.appendChild(studentsAppearedHeader);
                tableBody.appendChild(tableHeader);
                // add table rows
                
                data.report.forEach(item => {
                    const row = document.createElement('tr');
                    const subjectName = document.createElement('td');
                    subjectName.innerText = item.subject_name;
                    const passPercentage = document.createElement('td');
                    passPercentage.innerText = item.pass_percentage;
                    const studentsAppeared = document.createElement('td');
                    studentsAppeared.innerText = item.total_count;

                    row.appendChild(subjectName);
                    row.appendChild(passPercentage);
                    row.appendChild(studentsAppeared);
                    tableBody.appendChild(row);
                });


            // Create the chart
            const ctx = document.getElementById('myChart').getContext('2d');
            // Destroy the existing chart with ID '0'
            if (window.chart != undefined) {
                window.chart.destroy();
            }
            window.chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                label: 'Pass Percentage',
                data: passPercentages,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
                }]
            },
            options: {
                responsive: false,
            }
            });
        }
  
})
.catch(error => console.error(error));
}

generateReport();

const classDropdown = document.getElementById("class-dropdown");
const subjectDropdown = document.getElementById("subject-dropdown");

classDropdown.addEventListener("change", () => {
  const classId = classDropdown.value;
    const subjectId = subjectDropdown.value;
    generateReport(classId, subjectId);
  // call your function here with classId and subjectId as parameters
});

subjectDropdown.addEventListener("change", () => {
  const classId = classDropdown.value;
    const subjectId = subjectDropdown.value;
    generateReport(classId, subjectId);
  // call your function here with classId and subjectId as parameters
});