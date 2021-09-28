// async function geocodeAddress(geocoder, map) {
//     let input = document.getElementById("searchbar").value;
//     let new_search = {};
//     new_search.query = input;
//     $("#searchbar:text").val('');
//
//     const address = JSON.stringify(await submitInput(input));
//     geocoder.geocode({ address: address }, (results, status) => {
//         if (status === "OK") {
//             map.setCenter(results[0].geometry.location);
//             new google.maps.Marker({
//                 map: map,
//                 position: results[0].geometry.location,
//             });
//             let location = results[0].address_components[1].long_name;
//             let position = JSON.parse(JSON.stringify(results[0].geometry.location));
//
//             wiki(location, position, new_search);
//         } else {
//             alert("Geocode was not successful for the following reason: " + status);
//         }
//     });
// }
//
// function wiki(location, position, new_search) {
//
//     let url = "https://en.wikipedia.org/w/api.php";
//
//     let params = {
//         action: "query",
//         format: "json",
//         prop: "extracts",
//         list: "geosearch",
//         titles: location,
//         exsentences: "10",
//         exlimit: "1",
//         exintro: 1,
//         explaintext: 1,
//         gscoord: position.lat + "|" + position.lng,
//         gsradius: "1000",
//         gslimit: "1"
//     };
//
//     url = url + "?origin=*";
//     Object.keys(params).forEach(function(key){url += "&" + key + "=" + params[key];});
//
//     fetch(url)
//     .then(response => response.json())
//     .then(function(response) {
//         let wikiSearch = response.query.pages;
//         const wikiGeosearch = response.query.geosearch;
//
//         for (let place in wikiSearch) {
//             if (wikiSearch[place].hasOwnProperty('missing') === false && location === wikiSearch[place].title) {
//                 Object.assign(new_search, {
//                     wikiTitle: wikiSearch[place].title,
//                     wikiExtract: wikiSearch[place].extract,
//                     wikiUrl: "https://en.wikipedia.org/wiki/" + wikiSearch[place].title
//                 });
//             } else {
//                 for (let place in wikiGeosearch) {
//
//                     let url = "https://en.wikipedia.org/w/api.php";
//                     let params = {
//                         action: "query",
//                         format: "json",
//                         prop: "extracts",
//                         list: "",
//                         exsentences: "10",
//                         exlimit: "1",
//                         exintro: 1,
//                         explaintext: 1,
//                         pageids: wikiGeosearch[place].pageid,
//                     };
//
//                     url = url + "?origin=*";
//                     Object.keys(params).forEach(function (key) {
//                         url += "&" + key + "=" + params[key];
//                     });
//                     console.log(url)
//
//                     fetch(url)
//                     .then(response => response.json())
//                     .then(function(response) {
//                         let wikiSearch = response.query.pages;
//                         for (let place in wikiSearch) {
//                             new_search.wikiTitle = wikiSearch[place].title;
//                             new_search.wikiExtract = wikiSearch[place].extract;
//                             new_search.wikiUrl = "https://en.wikipedia.org/wiki/" + wikiSearch[place].title;
//                         }
//                     });
//                 }
//             }
//         }
//     })
//     .catch(function(error){console.log(error);});
//
//     formatNewSearch(new_search);
// }
