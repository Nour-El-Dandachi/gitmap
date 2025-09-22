import { render, screen, fireEvent } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { useSelector } from "react-redux";
import SideBar from "../components/shared/side-bar/index.jsx"; 

jest.mock("react-redux", () => ({
  useSelector: jest.fn(),
}));


const mockNavigate = jest.fn();
jest.mock("react-router-dom", () => ({
  ...jest.requireActual("react-router-dom"),
  useNavigate: () => mockNavigate,
  useLocation: () => ({ pathname: "/dashboard" }),
}));

describe("SideBar component", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    useSelector.mockImplementation(() => ({ user: { name: "Nour" } }));
  });

  test("renders logo and profile name", () => {
    render(
      <MemoryRouter>
        <SideBar />
      </MemoryRouter>
    );
    expect(screen.getByAltText("logo")).toBeInTheDocument();
    expect(screen.getByText("Nour")).toBeInTheDocument();
  });

  test("highlights Dashboard when on /dashboard", () => {
    render(
      <MemoryRouter>
        <SideBar />
      </MemoryRouter>
    );
    const dashboardItem = screen.getByText(/Dashboard/i).closest("div");
    expect(dashboardItem).toHaveClass("active");
  });

  test("navigates to My Repositories when clicked", () => {
    render(
      <MemoryRouter>
        <SideBar />
      </MemoryRouter>
    );
    const reposItem = screen.getByText(/My Repositories/i);
    fireEvent.click(reposItem);
    expect(mockNavigate).toHaveBeenCalledWith("/my-repositories");
  });

  test("navigates to Notifications when clicked", () => {
    render(
      <MemoryRouter>
        <SideBar />
      </MemoryRouter>
    );
    const notifItem = screen.getByText(/Notifications/i);
    fireEvent.click(notifItem);
    expect(mockNavigate).toHaveBeenCalledWith("/notifications");
  });

  test("navigates to Log out when clicked", () => {
    render(
      <MemoryRouter>
        <SideBar />
      </MemoryRouter>
    );
    const logoutItem = screen.getByText(/Log out/i);
    fireEvent.click(logoutItem);
    expect(mockNavigate).toHaveBeenCalledWith("/login");
  });
});
