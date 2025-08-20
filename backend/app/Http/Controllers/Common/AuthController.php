<?php

namespace App\Http\Controllers\Common;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Services\Common\AuthService;
use Exception;

class AuthController extends Controller
{
    public function login(Request $request){
        try{
            $user = AuthService::login($request);

            if($user){
                return $this->responseJSON($user);
            }

            return $this->responseJSON(null, 'Invalid credentials', 401);

        } catch (Exception $e){
            return $this->responseJSON(null, 'Login failed', 500);
        }
    }

    public function register(Request $request){
        try {
            $user = AuthService::register($request);

            if ($user) {
                return $this->responseJSON($user);
            }

            return $this->responseJSON(null, "Registration failed.", 400);
        } catch (Exception $e) {
            return $this->responseJSON(null, "Server error during registration.", 500);
        }
    }
}
