var config = {
    apiKey: "AIzaSyA_M-4o85aTaEy6VvjzCHJg7irezL7zrxE",
    authDomain: "wildfire-40a78.firebaseapp.com",
    databaseURL: "https://wildfire-40a78.firebaseio.com",
    projectId: "wildfire-40a78",
    storageBucket: "wildfire-40a78.appspot.com",
    messagingSenderId: "195705209280",
    appId: "1:195705209280:web:c1ed6135f37c06a2254825"
};


firebase.initializeApp(config);
var today = new Date().toLocaleString("sv", {timeZone: "America/Los_Angeles"}).slice(0, 10);
var date = today;
var features = [];
var view;






function drawMap(view, features, date) {
    require([
        "esri/Map",
        "esri/views/MapView",
        "esri/Graphic",
        "esri/layers/FeatureLayer",
        "esri/layers/GraphicsLayer",
        "esri/core/promiseUtils",
        "esri/geometry/Point",
        "esri/tasks/Locator",
        "esri/Color",
        "esri/renderers/SimpleRenderer",
        "esri/symbols/TextSymbol",
        "esri/symbols/Font",
        "esri/widgets/Search"
    ], function (Map,
                 MapView,
                 Graphic,
                 FeatureLayer,
                 GraphicsLayer,
                 promiseUtils,
                 Point,
                 Locator,
                 Color,
                 SimpleRenderer,
                 TextSymbol,
                 Font,
                 Search
    ) {

        view = new MapView({
            container: "viewDiv",
            map: new Map({
                basemap: "topo-vector",
            }),
            center: [-119.449438, 37.166062], // longitude, latitude
            zoom: 7,
        });

        var fireRenderer = {
            type: "simple",
            symbol: {
                type: "picture-marker",
                url: "https://www.flaticon.com/svg/static/icons/svg/870/870620.svg",
                width: "16px",
                height: "16px"
            }
        }

        // Search widget
        var search = new Search({
            view: view
        });

        view.ui.add(search, "top-right");

        function getData(callbackIN) {
            var ref = firebase.database().ref(date); //change to today
            ref.once('value').then(function (snapshot) {
                callbackIN(snapshot.val())
            })
                .then(checkFeatures)
                .then(createFeatureLayer)
                .then(addToView)
                .then(addToTable)
                .then(getSummaryData)
        };

        function genFunction(data) {
            var i = 1;
            Object.entries(data).forEach(([inst, valu]) => {
                features.push({
                    geometry: {type: "point", x: valu.Longitude, y: valu.Latitude},
                    attributes: {
                        ObjectID: i,
                        IncidentID: inst,
                        IncidentName: valu.IncidentName,
                        City: valu.City,
                        County: valu.County,
                        State: valu.State,
                        DiscoveryAcres: valu.DiscoveryAcres,
                        DailyAcres: valu.DailyAcres || "Unknown",
                        FireCause: valu.FireCause || "Unknown",
                        FireDiscoveryDateTime: valu.FireDiscoveryDateTime || "Unknown",
                        InitialResponseAcres: valu.InitialResponseAcres || "Unknown",
                        PercentContained: valu.PercentContained || "Unknown",
                        ContainmentDateTime: valu.ContainmentDateTime || "Unknown",
                        ControlDateTime: valu.ControlDateTime || "Unknown"
                    }
                });
                i += 1
            })
        };

        view.when()
            .then(getData(genFunction));

        function checkFeatures(){
            if (features.length == 0){
                addToTable();
            }
            else {
                return features;
            }
        }

        function createFeatureLayer() {
            var fireLayer = new FeatureLayer({
                source: features,  // array of graphics objects
                objectIdField: "ObjectID",
                fields: [
                    {name: "ObjectID", type: "oid"},
                    {name: "City", type: "string"},
                    {name: "ContainmentDateTime", type: "string"},
                    {name: "ControlDateTime", type: "string"},
                    {name: "County", type: "string"},
                    {name: "DailyAcres", type: "string"},
                    {name: "DiscoveryAcres", type: "string"},
                    {name: "FireCause", type: "string"},
                    {name: "FireDiscoveryDateTime", type: "string"},
                    {name: "IncidentID", type: "string"},
                    {name: "IncidentName", type: "string"},
                    {name: "InitialResponseAcres", type: "string"},
                    {name: "PercentContained", type: "string"},
                    {name: "State", type: "string"},
                ],
                popupTemplate: {
                    title: "{City}, {County}",
                    content: [{
                        type: "fields", fieldInfos: [
                            {fieldName: "IncidentID", label: "Incident ID"},
                            {fieldName: "IncidentName", label: "Incident Name"},
                            {fieldName: "DailyAcres", label: "Daily Acres"},
                            {fieldName: "DiscoveryAcres", label: "Discovery Acres"},
                            {fieldName: "FireCause", label: "Fire Cause"},
                            {fieldName: "FireDiscoveryDateTime", label: "Fire Discovery DateTime"},
                            {fieldName: "InitialResponseAcres", label: "Initial Response Acres"},
                            {fieldName: "PercentContained", label: "Percent Contained"}//,
                            //{fieldName:"ContainmentDateTime",label:"Containment DateTime"},
                            //{fieldName:"ControlDateTime",label:"Control DateTime"}
                        ]
                    }]
                },
                renderer: fireRenderer,
            });
            search.sources.push({
                layer: fireLayer,
                searchFields: ["IncidentName"],
                displayField: "IncidentName",
                exactMatch: false,
                outFields: ["IncidentName"],
                resultGraphicEnabled: true,
                name: "Incident Name",
            });
            view.ui.add(search, "top-right");
            return fireLayer;
        }

        // Adds a given layer to the map in the view
        function addToView(layer) {
            view.map.add(layer);
        }

        function addToTable() {
            var len = features.length;
            var tbody = document.getElementById("tbody");
            tbody.innerHTML = "";

            for (var i = 0; i < len; i++) {
                var row = getDataRow(features[i].attributes);
                tbody.appendChild(row);
            };
        }


        function getDataRow(row) {
            var tr = document.createElement("tr");

            var td0 = document.createElement("td");
            td0.innerHTML = row.ObjectID;
            tr.appendChild(td0);
            var td1 = document.createElement("td");
            td1.innerHTML = row.IncidentName;
            tr.appendChild(td1);
            var td2 = document.createElement("td");
            td2.innerHTML = row.IncidentID;
            tr.appendChild(td2);
            var td3 = document.createElement("td");
            td3.innerHTML = row.DailyAcres;
            tr.appendChild(td3);

            var td4 = document.createElement("td");
            td4.innerHTML = row.DiscoveryAcres;
            tr.appendChild(td4);
            var td5 = document.createElement("td");
            td5.innerHTML = row.FireCause;
            tr.appendChild(td5);
            var td6 = document.createElement("td");
            td6.innerHTML = row.FireDiscoveryDateTime;
            tr.appendChild(td6);
            var td7 = document.createElement("td");
            td7.innerHTML = row.InitialResponseAcres;
            tr.appendChild(td7);
            var td8 = document.createElement("td");
            td8.innerHTML = row.City;
            tr.appendChild(td8);
            var td9 = document.createElement("td");
            td9.innerHTML = row.County;
            tr.appendChild(td9);
            var td10 = document.createElement("td");
            td10.innerHTML = row.State;
            tr.appendChild(td10);
            var td11 = document.createElement("td");
            td11.innerHTML = row.ContainmentDateTime;
            tr.appendChild(td11);
            var td12 = document.createElement("td");
            td12.innerHTML = row.PercentContained;
            tr.appendChild(td12);
            var td13 = document.createElement("td");
            td13.innerHTML = row.ControlDateTime;
            tr.appendChild(td13);

            return tr;
        }


        function getSummaryData(){
            var url = 'http://4de639217b0f.ngrok.io/data?date='+date
            var httpRequest = new XMLHttpRequest();
            httpRequest.open("POST",url,true);
            httpRequest.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
            httpRequest.setRequestHeader("Access-Control-Allow-Origin", '*');
            httpRequest.setRequestHeader("Access-Control-Allow-Headers", 'x-requested-with');
            httpRequest.setRequestHeader("Access-Control-Allow-Methods", 'OPTIONS,POST,GET');
            httpRequest.setRequestHeader("Access-Control-Allow-Credentials", true);
            httpRequest.onreadystatechange = ()=>{
                if(httpRequest.readyState == 4 && httpRequest.status == 200){
                    var data = eval(httpRequest.responseText);
                    addToSummary(data);
                }
            }
            httpRequest.send();
        };


        function addToSummary(data){
            var groupbody = document.getElementById("groupbody");
            var idx_group = 1;
            groupbody.innerHTML = "";

            for (var val in data) {
                var tr = document.createElement("tr");
                var td0 = document.createElement("td");
                td0.innerHTML = idx_group;
                tr.appendChild(td0);
                var td1 = document.createElement("td");
                td1.innerHTML = data[val][0];
                tr.appendChild(td1);
                var td2 = document.createElement("td");
                td2.innerHTML = data[val][1];
                tr.appendChild(td2);
                idx_group += 1;

                groupbody.appendChild(tr);
            }
        };
    });
}

drawMap(view, features, date)