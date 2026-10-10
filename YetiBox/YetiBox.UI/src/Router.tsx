import { Route, Routes } from "react-router";
import AppComponent from "./App";
import HomeComponent from "./features/home/Home";
import CameraComponent from "./features/camera/Camera";
import ConfigComponent from "./features/config/Config";

export function YetiBoxRouter() {
    return (
        <Routes>
            <Route element={<AppComponent />}>
                <Route index element={<HomeComponent />} />
                <Route path="camera" element={<CameraComponent />} />
                <Route path="config" element={<ConfigComponent />} />
            </Route>
        </Routes>
    );
}