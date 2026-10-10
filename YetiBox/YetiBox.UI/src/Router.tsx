import { Route, Routes } from "react-router";
import AppComponent from "./App";
import CameraComponent from "./features/camera/Camera";
import ConfigComponent from "./features/config/Config";

export function YetiBoxRouter() {
    return (
        <Routes>
            <Route path="*" element={<AppComponent />} />
            <Route path="/camera" element={<CameraComponent />} />
            <Route path="/config" element={<ConfigComponent />} />
        </Routes>
    );
}