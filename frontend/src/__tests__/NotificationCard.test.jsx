import { render, screen, fireEvent } from "@testing-library/react";
import NotificationCard from "../components/notification-card/index.jsx";

describe("NotificationCard component", () => {
  const baseProps = {
    id: 1,
    message: "New repo added!",
    is_read: false,
    created_at: new Date().toISOString(),
    onMarkRead: jest.fn(),
  };

  test("renders message text", () => {
    render(<NotificationCard {...baseProps} />);
    expect(screen.getByText("New repo added!")).toBeInTheDocument();
  });

  test("shows 'Just now' for very recent notifications", () => {
    render(<NotificationCard {...baseProps} />);
    expect(screen.getByText("Just now")).toBeInTheDocument();
  });

  test("applies 'unread' class when is_read is false", () => {
    const { container } = render(<NotificationCard {...baseProps} />);
    expect(container.querySelector(".notification-card")).toHaveClass("unread");
  });

  test("applies 'read' class when is_read is true", () => {
    const { container } = render(<NotificationCard {...baseProps} is_read />);
    expect(container.querySelector(".notification-card")).toHaveClass("read");
  });

  test("calls onMarkRead when 'Mark as read' is clicked", () => {
    render(<NotificationCard {...baseProps} />);
    fireEvent.click(screen.getByText(/Mark as read/i));
    expect(baseProps.onMarkRead).toHaveBeenCalledWith(1);
  });
});
