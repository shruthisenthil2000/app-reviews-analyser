import { google } from "googleapis";
import { NextRequest, NextResponse } from "next/server";

export const runtime = "nodejs";

type DraftRequest = {
  to?: string;
  subject?: string;
  body?: string;
};

function encodeMessage(message: string): string {
  return Buffer.from(message)
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

export async function POST(request: NextRequest) {
  try {
    const payload = (await request.json()) as DraftRequest;

    const to = payload.to?.trim();
    const subject = payload.subject?.trim();
    const body = payload.body?.trim();

    if (!to || !subject || !body) {
      return NextResponse.json(
        {
          success: false,
          error: "To, subject and body are required.",
        },
        { status: 400 }
      );
    }

    const {
      GOOGLE_CLIENT_ID,
      GOOGLE_CLIENT_SECRET,
      GOOGLE_REFRESH_TOKEN,
      GMAIL_ACCOUNT,
    } = process.env;

    if (
      !GOOGLE_CLIENT_ID ||
      !GOOGLE_CLIENT_SECRET ||
      !GOOGLE_REFRESH_TOKEN ||
      !GMAIL_ACCOUNT
    ) {
      return NextResponse.json(
        {
          success: false,
          error: "Missing Google OAuth environment variables.",
        },
        { status: 500 }
      );
    }

    const auth = new google.auth.OAuth2(
      GOOGLE_CLIENT_ID,
      GOOGLE_CLIENT_SECRET
    );

    auth.setCredentials({
      refresh_token: GOOGLE_REFRESH_TOKEN,
    });

    const gmail = google.gmail({
      version: "v1",
      auth,
    });

    const message = [
      `From: ${GMAIL_ACCOUNT}`,
      `To: ${to}`,
      `Subject: ${subject}`,
      "MIME-Version: 1.0",
      'Content-Type: text/plain; charset="UTF-8"',
      "",
      body,
    ].join("\r\n");

    const encodedMessage = encodeMessage(message);

    const response = await gmail.users.drafts.create({
      userId: "me",
      requestBody: {
        message: {
          raw: encodedMessage,
        },
      },
    });

    return NextResponse.json({
      success: true,
      draftId: response.data.id,
      message: "Draft created successfully.",
    });
  } catch (error: any) {
    console.error(error);

    return NextResponse.json(
      {
        success: false,
        error: error.message ?? "Unknown error",
      },
      { status: 500 }
    );
  }
}