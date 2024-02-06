import React from "react";
import Map from "./map";
import { useLoadScript } from "@react-google-maps/api";
import { forwardRef } from "react";

export default forwardRef(function MapModal(props, ref) {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: "your-google-maps-api-key",
    libraries: ["places"],
  });

  if (!isLoaded) return <div>Loading...</div>;
  return (
    <dialog ref={ref} className="fixed bg-white rounded-md mb-32 shadow-md w-1/2 h-1/2 mt-40">
      <div className="fixed top-0 left-0 right-0 bg-slate-700 text-white p-4 flex justify-between items-center">
        <button className="text-white rounded-md" onClick={props.onClose}>
          Close
        </button>
        <button className="text-white rounded-md" onClick={(e)=>props.onFinish(e,"start chat")}>
          Start Analysis
        </button>
      </div>
      <Map handelClick={props.handelClick}/>
    </dialog>
  );
});
{
  /* <dialog open className="bg-white p-8 rounded-md shadow-md w-96">
        <h1 className="text-2xl font-bold mb-4">Map</h1>
        <p className="text-gray-600 mb-4">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
          facilisi. Proin tincidunt turpis vitae ultricies cursus. Fusce
          suscipit, felis vitae luctus mattis, sapien elit vestibulum libero,
          nec viverra ipsum nisi nec libero.
        </p>
        <form onSubmit={(e) => e.preventDefault()} method="dialog">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          >
            Close
          </button>
        </form>
      </dialog> */
}