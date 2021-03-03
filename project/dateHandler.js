function changeDate(e) {
    var date = e.target.value;
    var features = [];
    drawMap(view, features, date)
        // .then(addToTable(features));
}

function searchFunction() {
    var input, filter, table, tr, td, i;
    input = document.getElementById("searchvalue");
    filter = input.value.toUpperCase();

    table = document.getElementById("querytable");
    let content = table.getElementsByTagName("tbody")[0];
    tr = content.getElementsByTagName("tr");
    console.log(tr.length)

    for (i = 0; i < tr.length; i++) {
        tds = tr[i].getElementsByTagName("td");
        flag = 0;
        if (tds) {
            console.log(filter)
            for (j=0;j<tds.length;j++) {
                td = tds.item(j);
                if (td.innerHTML.toUpperCase().includes(filter)) {//.indexOf(filter) > -1) {
                    flag = 1;
                }
            }
            if (flag==1){
                tr[i].style.display = "";
            }else {
                tr[i].style.display = "none";
            }
        }
    };
}