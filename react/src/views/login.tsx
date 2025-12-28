import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import Header from "../components/header";
import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import utils from "../utils/utils";

type LoginForm = {
  email: string;
  password: string;
};

function Login() {
  const navigate = useNavigate();
  const { setIdToken } = userStore();
  const { setLoading } = loadingState();

  const [loginError, setLoginError] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setLoading(true);
    setLoginError(false);

    const res_promise = utils.requests(
      `${import.meta.env.VITE_API_HOST}/login`,
      "POST",
      {},
      {
        email: data.email,
        password: data.password,
      }
    );
    const res = await res_promise;

    if (res.status != 200) {
      setLoading(false);
      setLoginError(true);
      throw new Error(`login error`);
    };

    const body = res.body as { id_token: string };
    setIdToken(body.id_token);
    navigate("/main?node_id=/Nodes");
  };

  return (
    <>
      <title>Login</title>
      <Header />

      <Container
        maxWidth="xs"
        sx={{
          marginTop: 8,
          border: "1px solid #ddd",
          borderRadius: "10px",
          padding: "20px",
        }}
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <Typography variant="h4" align="center">
            Login
          </Typography>

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

          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ marginTop: "5%" }}
          >
            ログイン
          </Button>

          {loginError && (
            <Alert severity="error" sx={{ mt: 2 }}>
              メールアドレスまたはパスワードが正しくありません
            </Alert>
          )}
        </form>
      </Container>
    </>
  );
};

export default Login;