import { render, screen, fireEvent } from "@testing-library/react";
import Input from "../components/shared/input/index.jsx"; 

describe("Input component", () => {
  test("renders with placeholder text", () => {
    render(<Input type="text" name="username" hint="Enter your username" icon="user" />);
    expect(screen.getByPlaceholderText("Enter your username")).toBeInTheDocument();
  });

  test("renders mail icon when icon='mail'", () => {
    const { container } = render(<Input type="email" name="email" hint="Enter email" icon="mail" />);
    expect(screen.getByPlaceholderText("Enter email")).toBeInTheDocument();
    expect(container.querySelector("svg.lucide-mail")).toBeInTheDocument();
  });

  test("calls onChange when typing", () => {
    const handleChange = jest.fn();
    render(<Input type="text" name="username" hint="Username" icon="user" onChange={handleChange} />);
    
    const input = screen.getByPlaceholderText("Username");
    fireEvent.change(input, { target: { value: "Nour" } });

    expect(handleChange).toHaveBeenCalledTimes(1);
  });

  test("renders with value prop", () => {
    render(<Input type="text" name="username" hint="Username" icon="user" value="Nour" onChange={() => {}} />);
    expect(screen.getByDisplayValue("Nour")).toBeInTheDocument();
  });
});