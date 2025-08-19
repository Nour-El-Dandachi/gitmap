<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Common\GithubAuthController;

Route::get('/auth/github/redirect', [GithubAuthController::class, 'redirect']);
Route::get('/auth/github/callback', [GithubAuthController::class, 'callback']);


Route::get('/', function () {
    return view('welcome');
});
