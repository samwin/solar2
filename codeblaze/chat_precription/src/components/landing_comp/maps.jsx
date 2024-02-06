import { useState, useMemo, useCallback, useRef } from "react";
import {
  GoogleMap,
  MarkerF,
} from "@react-google-maps/api";

const handelClick = async (value1, value2) => {
    const response = await fetch("http://127.0.0.1:8000/product", {
        method : "POST",       
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'text': `${value1},${value2}`})
    })
}



export default function Map() {
    
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
    console.log('chicled')
    const value1 = event.latLng.lat()
    const value2 = event.latLng.lng()
    handelClick(value1, value2)
    
    console.log(event.latLng.lat())
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