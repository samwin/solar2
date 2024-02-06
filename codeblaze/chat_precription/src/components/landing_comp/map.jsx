import { useState, useMemo, useCallback, useRef } from "react";
import {
  GoogleMap,
  MarkerF,
} from "@react-google-maps/api";

// const handelClick = async (value1, value2) => {
//     const response = await fetch("https://9742-106-193-17-66.ngrok.io/get_data", {
//         method : "POST",       
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({'text': `${value1},${value2}`})
//     })
//     const data = await response.json()
//     console.log(data)
// }



export default function Map(props) {
    
  const mapRef = useRef();

  const center = useMemo(
    () => ({ lat:  12.915605, lng: 74.855965 }),
    []
  );
  const options = useMemo(
    () => ({
      // disableDefaultUI: true,
      clickableIcons: false,
    }),
    []
  );
  const onLoad = useCallback((map) => (mapRef.current = map), []);


  const [marker, setMarker] = useState(null);
//   const { marker, setMarker } = useMapContext();

  const onMapClick = (event) => {
    console.log('chicked')
    const value1 = event.latLng.lat()
    const value2 = event.latLng.lng()
    props.handelClick(event, value1, value2)
    
    console.log(value1, value2)
    setMarker({
      lat: event.latLng.lat(),
      lng: event.latLng.lng(),
    });
  };

  return (
    <div className="container">
      <div className="map">
        <GoogleMap
          zoom={10}
          center={center}
          mapContainerClassName="map-container"
           mapContainerStyle={{ height: "1300px", width: "150%" }}
          options={options}
          onLoad={onLoad}
          onClick={onMapClick}
        >
        {marker && <MarkerF position = {marker} />}
        </GoogleMap>
      </div>
    </div>
  );
}