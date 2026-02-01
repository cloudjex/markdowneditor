import { Alert, Button, Container, Dialog, DialogTitle, TextField } from "@mui/material";
import { MuiOtpInput } from 'mui-one-time-password-input';
import { useState } from "react";
import { useForm } from "react-hook-form";

import type { SignupForm } from "@/src/lib/types";

import RequestHandler from "@/src/lib/request_handler";
import loadingState from "@/src/store/loading_store";


function Signup() {
  const { setLoading } = loadingState();

  const [newUser, setNewUser] = useState({
    email: "",
    password: "",
    passwordConfirm: "",
    pwMatch: true,
    otp: "",
  });

  const { register, handleSubmit, formState: { errors } } = useForm<SignupForm>();

  const [signupError, setSignupError] = useState(false);
  const [verifyError, setVerifyError] = useState(false);
  // 0: null, 1: verify
  const [modalKind, setModalKind] = useState(0);

  const requests = new RequestHandler();

  async function onSignupSubmit(data: SignupForm) {
    setNewUser({
      ...newUser,
      email: data.email,
      password: data.password,
      passwordConfirm: data.password_confirm,
      pwMatch: data.password === data.password_confirm,
    });
    setSignupError(false);

    if (data.password !== data.password_confirm) {
      throw new Error("password mismatch");
    }

    setLoading(true);

    const res = await requests.post(
      `${import.meta.env.VITE_API_HOST}/api/signup`,
      { email: data.email, password: data.password }
    );

    setLoading(false);

    if (res.status != 200) {
      setSignupError(true);
      throw new Error("signup error");
    };

    setModalKind(1);
  };

  async function onVerifySubmit() {
    if (newUser.otp.length < 6) {
      setVerifyError(true);
      throw new Error("invalid otp");
    }

    setVerifyError(false);
    setModalKind(0);
    setLoading(true);

    const normalized_otp = newUser.otp.replace(/[０-９]/g, s => String.fromCharCode(s.charCodeAt(0) - 0xFEE0));

    const res = await requests.post(
      `${import.meta.env.VITE_API_HOST}/api/signup/verify`,
      { email: newUser.email, otp: normalized_otp }
    );

    setLoading(false);

    if (res.status != 200) {
      setModalKind(1);
      setVerifyError(true);
      throw new Error("signup error");
    };

    // reload
    window.location.reload();
  };

  return (
    <>
      <form onSubmit={handleSubmit(onSignupSubmit)}>
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
          {...register("password_confirm", {
            required: "パスワード(確認用)は必須です",
          })}
          error={!!errors.password_confirm}
          helperText={errors.password_confirm?.message}
        />

        <Button
          type="submit"
          fullWidth
          variant="contained"
          sx={{ mt: 3 }}
        >
          ユーザ登録
        </Button>

        {newUser.pwMatch === false && (
          <Alert severity="error" sx={{ mt: 2 }}>
            パスワードが一致しません
          </Alert>
        )}
        {signupError && (
          <Alert severity="error" sx={{ mt: 2 }}>
            ユーザ登録に失敗しました
          </Alert>
        )}
      </form>

      <Dialog
        open={modalKind == 1}
      >
        <Container>
          <DialogTitle
            variant="body1"
          >
            メールアドレスに送付された認証コードを入力してください
          </DialogTitle>

          <form onSubmit={handleSubmit(onVerifySubmit)}>

            <MuiOtpInput
              value={newUser.otp}
              onChange={(value) => setNewUser({ ...newUser, otp: value })}
              length={6}
              autoFocus
              sx={{ m: 5 }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mb: 3 }}
            >
              送信
            </Button>

            {verifyError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                認証コードが正しくありません
              </Alert>
            )}

          </form>
        </Container>
      </Dialog >
    </>
  );
};

export default Signup;