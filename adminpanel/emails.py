from django.core.mail import send_mail
from django.conf import settings


def _send(to_email: str, subject: str, body: str):
    """Internal helper — silently swallows errors so a mail failure never breaks the API."""
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
    except Exception as exc:
        # Log to console so you can see it in Render logs, but don't crash
        print(f"[EMAIL ERROR] Failed to send to {to_email}: {exc}")


def send_instructor_approved(user):
    _send(
        to_email=user.email,
        subject="🎉 Your EduCore AI Instructor Account is Approved!",
        body=(
            f"Hi {user.first_name or user.username},\n\n"
            "Great news! Your instructor account on EduCore AI has been approved by our admin team.\n\n"
            "You can now log in and start creating courses:\n"
            "👉 https://educore-ai.vercel.app/login\n\n"
            "Welcome aboard!\n"
            "— The EduCore AI Team"
        ),
    )


def send_instructor_rejected(user, reason: str = ""):
    reason_block = f"\n\nReason: {reason}" if reason.strip() else ""
    _send(
        to_email=user.email,
        subject="EduCore AI — Instructor Application Update",
        body=(
            f"Hi {user.first_name or user.username},\n\n"
            "After review, we were unable to approve your instructor application at this time."
            f"{reason_block}\n\n"
            "If you believe this is a mistake or would like to appeal, please reply to this email.\n\n"
            "— The EduCore AI Team"
        ),
    )


def send_user_deleted(email: str, username: str, reason: str = ""):
    reason_block = f"\n\nReason: {reason}" if reason.strip() else ""
    _send(
        to_email=email,
        subject="EduCore AI — Your Account Has Been Removed",
        body=(
            f"Hi {username},\n\n"
            "Your EduCore AI account has been removed by an administrator."
            f"{reason_block}\n\n"
            "If you have questions, please contact support.\n\n"
            "— The EduCore AI Team"
        ),
    )


def send_course_deleted(instructor_email: str, instructor_name: str, course_title: str, reason: str = ""):
    reason_block = f"\n\nReason: {reason}" if reason.strip() else ""
    _send(
        to_email=instructor_email,
        subject=f"EduCore AI — Course Removed: {course_title}",
        body=(
            f"Hi {instructor_name},\n\n"
            f'Your course "{course_title}" has been removed by an EduCore AI administrator.'
            f"{reason_block}\n\n"
            "If you have questions, please contact support.\n\n"
            "— The EduCore AI Team"
        ),
    )