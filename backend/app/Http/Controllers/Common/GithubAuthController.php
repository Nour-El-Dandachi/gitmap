<?php

namespace App\Http\Controllers\Common;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Laravel\Socialite\Facades\Socialite;
use App\Http\Controllers\Common\AuthController;
use App\Services\Common\GithubAuthService;

class GithubAuthController extends Controller
{

    public function redirect()
    {
        return Socialite::driver('github')->redirect();
    }

    public function callback()
    {
        $user = GithubAuthService::callback();
        return $this->responseJSON($user);
    }
}
