import { Alert, Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from "@mui/material";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import RequestHandler from "@/lib/request_handler";
import type { SignupForm } from "@/lib/types";
import loadingState from "@/store/loading_store";
import userStore from '@/store/user_store';


function Signup() {
  const { resetUserState, email, setEmail } = userStore();
  const { setLoading, resetLoadingState } = loadingState();
  const [signupError, setSignupError] = useState(false);
  const { register, handleSubmit, formState: { errors } } = useForm<SignupForm>();

  // for otp dialog
  const [otp, setOtp] = useState("");
  const [otpDialogOpen, setOtpDialogOpen] = useState(false);
  const [verifyError, setVerifyError] = useState(false);

  useEffect(() => {
    resetUserState();
    resetLoadingState();
  }, []);

  async function onSubmit(data: SignupForm) {
    if (data.password !== data.passwordConfirm) {
      setSignupError(true);
      throw new Error("signup error");
    };

    setLoading(true);
    setSignupError(false);

    const requests = new RequestHandler();
    const signupRes = await requests.post(
      `/api/signup`,
      { email: data.email, password: data.password }
    );

    if (signupRes.status != 200) {
      setSignupError(true);
      setLoading(false);
      throw new Error("signup error");
    };

    setEmail(data.email);
    setLoading(false);

    setOtpDialogOpen(true);
  };

  async function verifyEmail(otp: string) {
    if (otp.length === 0) {
      setVerifyError(true);
      throw new Error("verify error");
    }

    setLoading(true);
    setVerifyError(false);

    const requests = new RequestHandler();
    const verifyRes = await requests.post(
      `/api/signup/verify`,
      { otp: otp, email: email }
    );

    if (verifyRes.status != 200) {
      setVerifyError(true);
      setLoading(false);
      throw new Error("verify error");
    }

    setLoading(false);
    setOtpDialogOpen(false);

    window.location.reload();
  }

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
        <TextField
          label="メールアドレス"
          fullWidth
          margin="normal"
          {...register("email", {
            required: "メールアドレスは必須です",
          })}
          error={!!errors.email}
          helperText={errors.email?.message}
        />

        <TextField
          label="パスワード"
          type="password"
          fullWidth
          margin="normal"
          {...register("password", {
            required: "パスワードは必須です",
          })}
          error={!!errors.password}
          helperText={errors.password?.message}
        />

        <TextField
          label="パスワード(確認用)"
          type="password"
          fullWidth
          margin="normal"
          {...register("passwordConfirm", {
            required: "パスワード(確認用)は必須です",
          })}
          error={!!errors.passwordConfirm}
          helperText={errors.passwordConfirm?.message}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3 }}
        >
          サインアップ
        </Button>

        {signupError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            サインアップに失敗しました
          </Alert>
        )}
      </form>

      {otpDialogOpen && (
        <Dialog
          open={otpDialogOpen}
          onClose={() => setOtpDialogOpen(false)}
        >
          <DialogTitle
            sx={{ fontSize: "1rem" }}
          >
            メールアドレスに送信されたOTPを入力してください
          </DialogTitle>

          <DialogContent>
            <TextField
              label="OTP"
              fullWidth
              margin="normal"
              onChange={(e) => setOtp(e.target.value)}
            />

            {verifyError && (
              <Alert severity="error" sx={{ mt: 2 }}>
                メール認証に失敗しました
              </Alert>
            )}
          </DialogContent>

          <DialogActions>
            <Button onClick={() => verifyEmail(otp)}>OK</Button>
          </DialogActions>
        </Dialog>
      )}
    </>
  );
};

export default Signup;
