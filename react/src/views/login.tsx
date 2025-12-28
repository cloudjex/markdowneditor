import Alert from "@mui/material/Alert";
import Button from "@mui/material/Button";
import Container from "@mui/material/Container";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useState } from 'react';
import { useNavigate } from "react-router-dom";

import Header from "../components/header";
import loadingState from "../store/loading_store";
import userStore from '../store/user_store';
import utils from "../utils/utils";

function Login() {
  const navigate = useNavigate();

  const { email, setEmail, password, setPassword, setIdToken } = userStore();
  const { setLoading } = loadingState();
  const [isLoginError, setLoginError] = useState(false);

  const handleEmailChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setEmail(event.target.value);
  };

  const handlePwChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(event.target.value);
  };

  const onClickSignin = async () => {
    setLoading(true);

    const res_promise = utils.requests(
      `${import.meta.env.VITE_API_HOST}/login`,
      "POST",
      {},
      {
        email: email,
        password: password,
      }
    );
    const res = await res_promise;

    if (res.status != 200) {
      setLoginError(true);
      setLoading(false);
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

      <Container maxWidth="xs" sx={{ marginTop: 10, border: '1px solid #ddd', borderRadius: '10px', padding: '30px' }}>

        <Typography variant="h4" align="center">
          Login
        </Typography>

        <TextField
          value={email}
          onChange={handleEmailChange}
          margin="normal"
          fullWidth
          label="メールアドレス"
        />

        <TextField
          value={password}
          onChange={handlePwChange}
          margin="normal"
          fullWidth
          label="パスワード"
          type="password"
          autoComplete="current-password"
        />

        <Button
          onClick={onClickSignin}
          fullWidth
          variant="contained"
          sx={{ marginTop: "5%" }}
        >
          ログイン
        </Button>

        {isLoginError &&
          <Alert severity="error">IDまたはパスワードが正しくありません</Alert>
        }

      </Container>
    </>
  );
};

export default Login;